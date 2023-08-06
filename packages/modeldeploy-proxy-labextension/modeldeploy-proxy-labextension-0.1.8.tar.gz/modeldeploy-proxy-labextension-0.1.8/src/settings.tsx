import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';
import { Kernel } from '@jupyterlab/services';
import NotebookUtils from './lib/NotebookUtils';

export const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';

export const getTransformerEnabled = (settings: ISettingRegistry.ISettings): boolean => {
    try {
        let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
        if(typeof transformerSettings.enabled === 'string' && transformerSettings.enabled === 'true') {
            return true;
        } else if(typeof transformerSettings.enabled === 'boolean') {
            return transformerSettings.enabled
        }
    } catch (error) {
        console.error(error);
    }
    return false;
};

export const setTransformerEnabled = (settings: ISettingRegistry.ISettings, enabled: boolean) => {
    let config : IConfig = {
        enabled: enabled
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerNotebookDir = (settings: ISettingRegistry.ISettings): string => {
    try {
        let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
        if(typeof transformerSettings.notebookDir === 'string') {
            return transformerSettings.notebookDir;
        }
    } catch (error) {
        console.error(error);
    }
    return "";
};

export const setTransformerNotebookDir = (settings: ISettingRegistry.ISettings, notebookDir: string) => {
    let config : IConfig = {
        notebookDir: notebookDir
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerProxyUrl = (settings: ISettingRegistry.ISettings): string => {
    try {
        let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
        if(typeof transformerSettings.proxyUrl === 'string') {
            return transformerSettings.proxyUrl;
        } else if(typeof transformerSettings.proxyUrl === 'number') {
            return transformerSettings.proxyUrl.toString();
        }
    } catch (error) {
        console.error(error);
    }
    return "";
};

export const setTransformerProxyUrl = (settings: ISettingRegistry.ISettings, proxyUrl: string) => {
    let config : IConfig = {
        proxyUrl: proxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

interface IConfig {
    enabled?: boolean;
    notebookDir?: string;
    proxyUrl?: string;
}

const kernelCmd: string = `
import os
dir = os.getcwd()
proxy = ""
PROXY_URL_NAME = ".proxy"
try:
    for root, dirs, files in os.walk(dir):
        if PROXY_URL_NAME in files:
            path = os.path.join(root, PROXY_URL_NAME)
            proxy = open(path).readline().strip()
            break
except Exception:
    pass
`

const defaultConfig: IConfig = {
    enabled: false,
    notebookDir: "",
    proxyUrl: ""
}

export default {
    id: SETTINGS_ID,
    requires: [ ISettingRegistry ],
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry
    ): void => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(async ([settings]) => {
            let enabled: boolean;
            let notebookDir: string = "";
            let proxyUrl: string = "";
            try {
                enabled = getTransformerEnabled(settings);
                notebookDir = getTransformerNotebookDir(settings);
                proxyUrl = getTransformerProxyUrl(settings);
            } catch (error) {
                settingRegistry.set(SETTINGS_ID, TRFANFORMER_CONFIG, defaultConfig as unknown as JSONObject).catch((reason: Error) => {
                    console.error('Failed to set transformer config: ' + reason.message);
                });
            }
            try {
                const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
                let output: any = await NotebookUtils.sendKernelRequest(kernel, kernelCmd, { dir: 'dir', proxy: 'proxy' }, true);
                let dir = output.dir.data['text/plain'];
                dir = dir.replaceAll("'", "")
                console.log("Init directory: " + dir);
                if(dir && dir !== notebookDir) {
                    setTransformerNotebookDir(settings, dir);
                    notebookDir = dir;
                }
                let proxy = output.proxy.data['text/plain'];
                proxy = proxy.replaceAll("'", "")
                console.log("Init proxy: " + proxy);
                if(proxy && proxy !== proxyUrl) {
                    setTransformerProxyUrl(settings, proxy);
                    proxyUrl = proxy;
                }
            } catch (e) {
                console.warn(e);
            }
            console.log("Settings when starts up: enabled(" + enabled + "), NotebookDir(" + notebookDir + "), ProxyUrl(" + proxyUrl + ")");
        });
    },
} as JupyterFrontEndPlugin<void>;
