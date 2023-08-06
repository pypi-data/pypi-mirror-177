import * as React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import { theme } from './../theme';
import { executeRpc, globalUnhandledRejection } from './../lib/RPCUtils';
import NotebookUtils from './../lib/NotebookUtils';
import { Kernel } from '@jupyterlab/services';
import { Switch } from '@material-ui/core';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled, setTransformerEnabled, getTransformerProxyUrl } from './../settings';
import { getTransformerNotebookDirectory } from './../notebook';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@material-ui/core';

interface IProps {
    transformerSettings: ISettingRegistry.ISettings
}

interface IState {
    isEnabled: boolean;
    dialogTitle: string;
    dialogContent: string;
    isDialogVisible: boolean;
    isDialogButtonVisible: boolean;
}

export class TransformerLeftPanel extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        const defaultState: IState = {
            isEnabled: getTransformerEnabled(this.props.transformerSettings),
            isDialogVisible: false,
            isDialogButtonVisible: true,
            dialogTitle: '',
            dialogContent: ''
        };
        this.state = defaultState;
        this.onDialogCloseClick = this.onDialogCloseClick.bind(this);
    }

    onDialogCloseClick() {
        this.setState({ isDialogVisible: !this.state.isDialogVisible });
    }

    componentDidMount = () => {
        // Notebook tracker will signal when a notebook is changed
        console.log("transformerEnabled = " + getTransformerEnabled(this.props.transformerSettings));
    };

    componentDidUpdate = (
        prevProps: Readonly<IProps>,
        prevState: Readonly<IState>,
    ) => {
        console.log("componentDidUpdate");
    };

    applyTransformerToProxy = async () => {
        console.log('applyTransformerToProxy');
        this.setState({
            isDialogVisible: true,
            isDialogButtonVisible: false,
            dialogTitle: 'Running',
            dialogContent: 'It will take few seconds!'
        });

        let proxyUrl: string = getTransformerProxyUrl(this.props.transformerSettings);
        if(! proxyUrl) {
            this.setState({
                isDialogVisible: true,
                isDialogButtonVisible: true,
                dialogTitle: 'Error',
                dialogContent: 'Unable to get the proxy URL!'
            });
            return;
        }

        try {
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            const args = {
                proxy_url: proxyUrl,
                source_notebook_path: getTransformerNotebookDirectory()
            }
            const result = await executeRpc(kernel, 'proxy.apply', args);
            console.log(result);
            this.setState({
                isDialogVisible: true,
                isDialogButtonVisible: true,
                dialogTitle: 'Done',
                dialogContent: 'The transforming is completed!'
            });
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            this.setState({
                isDialogVisible: true,
                isDialogButtonVisible: true,
                dialogTitle: 'Error',
                dialogContent: error
            });
            throw error;
        }
    };

    onTransformerEnableChanged = (enabled: boolean) => {
        this.setState({ isEnabled: enabled });
        setTransformerEnabled(this.props.transformerSettings, enabled);
    };

    render() {
        return (
            <ThemeProvider theme={theme}>
                <div className={'leftpanel-transformer-widget'} key="transformer-widget" style={{padding: 'var(--jp-code-padding)'}}>
                    <div className={'leftpanel-transformer-widget-content'}>
                        <div className="transformer-header" style={{fontSize: 'var(--jp-ui-font-size3)'}} >
                            <p>Transformer Panel</p>
                        </div>

                        <div className='transformer-component' >
                            <div>
                                <p className="transformer-header" style={{ color: theme.transformer.headers.main, fontSize: 'var(--jp-ui-font-size1)'}}>
                                    Transformer is the extension for model inference, it injects pre and post preocessors defined in <strong style={{fontSize: 'var(--jp-ui-font-size2)'}}>transformer.ipynb</strong> notebook.
                                </p>
                            </div>
                        </div>

                        <div className="transformer-toggler">
                            <React.Fragment>
                                <div className="toolbar input-container">
                                    <Switch
                                        checked={this.state.isEnabled}
                                        onChange={c => this.onTransformerEnableChanged(c.target.checked)}
                                        color="primary"
                                        name="enable-transformer"
                                        inputProps={{ 'aria-label': 'primary checkbox' }}
                                        classes={{ root: 'material-switch' }}
                                    />
                                    <div className={'switch-label'} style={{ display: 'inline-block' }}>
                                        {(this.state.isEnabled ? 'Disable' : 'Enable') + ' transformer widgets'}
                                    </div>
                                </div>
                            </React.Fragment>
                        </div>

                        <div className={ 'transformer-component ' + (this.state.isEnabled ? '' : 'hidden') } >
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    title="Apply the changes."
                                    onClick={this.applyTransformerToProxy}
                                    disabled={ false }
                                    style={{ marginLeft: '10px', marginTop: '0px' }}
                                >
                                    Apply Changes
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
                <Dialog
                    open={this.state.isDialogVisible}
                    fullWidth={true}
                    maxWidth={'sm'}
                    scroll="paper"
                    aria-labelledby="scroll-dialog-title"
                    aria-describedby="scroll-dialog-description"
                >
                    <DialogTitle id="scroll-dialog-title">
                        <p className={'dialog-title'} >{this.state.dialogTitle}</p>
                    </DialogTitle>
                    <DialogContent dividers={true}>
                        <p>{this.state.dialogContent}</p>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            className={ 'transformer-dialog ' + (this.state.isDialogButtonVisible ? '' : 'hidden') }
                            color="primary"
                            onClick={this.onDialogCloseClick}
                        >Ok</Button>
                    </DialogActions>
                </Dialog>
            </ThemeProvider>
        );
    }
}
