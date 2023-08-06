import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';
import { Kernel } from '@jupyterlab/services';
import NotebookUtils from './lib/NotebookUtils';

export const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';

let transformerEnabled: boolean = false;
let transformerNotebookDir: string = "";
let transformerProxyUrl: string = "";

export const getTransformerEnabled = (): boolean => {
    return transformerEnabled;
};

export const setTransformerEnabled = (settings: ISettingRegistry.ISettings, enabled: boolean) => {
    transformerEnabled = enabled;
    let config : IConfig = {
        enabled: enabled,
        notebookDir: transformerNotebookDir,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerNotebookDir = (): string => {
    return transformerNotebookDir;
};

export const setTransformerNotebookDir = (settings: ISettingRegistry.ISettings, notebookDir: string) => {
    transformerNotebookDir = notebookDir;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookDir: notebookDir,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerProxyUrl = (): string => {
    return transformerProxyUrl;
};

export const setTransformerProxyUrl = (settings: ISettingRegistry.ISettings, proxyUrl: string) => {
    transformerProxyUrl = proxyUrl;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookDir: transformerNotebookDir,
        proxyUrl: proxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

interface IConfig {
    enabled: boolean;
    notebookDir: string;
    proxyUrl: string;
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
            try {
                let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
                if(typeof transformerSettings.enabled === 'string') {
                    if(transformerSettings.enabled === 'true') {
                        transformerEnabled = true;
                    } else {
                        transformerEnabled = false;
                    }
                } else if(typeof transformerSettings.enabled === 'boolean') {
                    transformerEnabled = transformerSettings.enabled
                }

                if(typeof transformerSettings.notebookDir === 'string') {
                    transformerNotebookDir = transformerSettings.notebookDir;
                }

                if(typeof transformerSettings.proxyUrl === 'string') {
                    transformerProxyUrl = transformerSettings.proxyUrl;
                } else if(typeof transformerSettings.proxyUrl === 'number') {
                    transformerProxyUrl = transformerSettings.proxyUrl.toString();
                }
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
                if(dir && dir !== transformerNotebookDir) {
                    console.log("Change notebook directory to: " + dir);
                    setTransformerNotebookDir(settings, dir);
                }
                let proxy = output.proxy.data['text/plain'];
                proxy = proxy.replaceAll("'", "")
                if(proxy && proxy !== transformerProxyUrl) {
                    console.log("Change proxy URL to: " + proxy);
                    setTransformerProxyUrl(settings, proxy);
                }
            } catch (e) {
                console.warn(e);
            }
            console.log("Settings when starts up: enabled(" + transformerEnabled + "), NotebookDir(" + transformerNotebookDir + "), ProxyUrl(" + transformerProxyUrl + ")");
        });
    },
} as JupyterFrontEndPlugin<void>;
