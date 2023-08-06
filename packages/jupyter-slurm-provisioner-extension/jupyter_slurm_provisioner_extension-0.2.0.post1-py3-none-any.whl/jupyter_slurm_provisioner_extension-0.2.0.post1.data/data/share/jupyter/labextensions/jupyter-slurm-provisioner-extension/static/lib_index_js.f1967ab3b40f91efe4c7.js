"use strict";
(self["webpackChunkjupyter_slurm_provisioner_extension"] = self["webpackChunkjupyter_slurm_provisioner_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI),
/* harmony export */   "sendGetRequest": () => (/* binding */ sendGetRequest),
/* harmony export */   "sendPostRequest": () => (/* binding */ sendPostRequest)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'slurm-provisioner', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function sendPostRequest(config) {
    let new_config = {
        jobid: String(config.allocation || "None"),
        node: String(config.node || "None"),
        kernel: config.kernel,
        kernel_argv: config.kernel_argv,
        kernel_language: config.kernel_language,
        project: String(config.project),
        partition: String(config.partition),
        nodes: String(config.nodes),
        gpus: String(config.gpus || 0),
        runtime: String(config.runtime),
        reservation: String(config.reservation || "None")
    };
    await requestAPI('configure', {
        body: JSON.stringify(new_config),
        method: "POST"
    }).catch(reason => {
        console.error(`Slurm-Provisioner: Could not save slurm-provisioner.\n${reason}`);
    });
}
async function sendGetRequest() {
    let config_system = {
        dropdown_lists: {},
        resources: {},
        allocations: {},
        documentationhref: "",
        current_config: {}
    };
    await requestAPI('configure').then(data => {
        config_system = data;
    }).catch(reason => {
        console.error(`Slurm-Configurator: Could not receive OptionsForm for user.\n${reason}`);
    });
    return config_system;
}


/***/ }),

/***/ "./lib/icon.js":
/*!*********************!*\
  !*** ./lib/icon.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "slurmelIcon": () => (/* binding */ slurmelIcon),
/* harmony export */   "slurmelIcon2": () => (/* binding */ slurmelIcon2)
/* harmony export */ });
/* harmony import */ var _style_slurmel_icon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/slurmel-icon.svg */ "./style/slurmel-icon.svg");
/* harmony import */ var _style_slurmel_icon_notebook_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/slurmel-icon-notebook.svg */ "./style/slurmel-icon-notebook.svg");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);



const slurmelIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'launcher:slurmel',
    svgstr: _style_slurmel_icon_svg__WEBPACK_IMPORTED_MODULE_1__["default"]
});
const slurmelIcon2 = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'launcher:slurmel2',
    svgstr: _style_slurmel_icon_notebook_svg__WEBPACK_IMPORTED_MODULE_2__["default"]
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar.js");
/* harmony import */ var _kernelSelector__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./kernelSelector */ "./lib/kernelSelector.js");
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widgets */ "./lib/widgets.js");


// import { ToolbarKernelButton, ToolbarCountdown } from './toolbar';






/**
 * The command IDs used by the react-widget plugin
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.slurmUI = 'slurm-config-ui';
    CommandIDs.dialog = 'open-slurm-config-dialog';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the slurm-provisioner-configurator extension.
 */
const extension = {
    id: 'slurm-provisioner-configurator',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: activate,
};
/**
 * Activate the JupyterLab extension.
 *
 * @param app
 * @param palette
 * @param launcher
 */
function activate(app, restorer, palette) {
    var _a;
    const { commands, shell, serviceManager } = app;
    const category = 'Slurm';
    // Load available kernels, excecpt the slurm one, in a list
    const available_kernels = (_a = serviceManager.kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs;
    let available_kernel_names = {};
    for (let key in available_kernels) {
        let kernel = available_kernels[key];
        try {
            if (kernel.metadata["kernel_provisioner"]["provisioner_name"] != "slurm-provisioner") {
                available_kernel_names[kernel.display_name] = kernel.argv;
            }
        }
        catch (error) {
            available_kernel_names[kernel.display_name] = kernel.argv;
        }
    }
    const slurmPanel = new _widgets__WEBPACK_IMPORTED_MODULE_2__.SlurmPanel(commands, available_kernel_names);
    restorer.add(slurmPanel, 'slurm-config');
    app.shell.add(slurmPanel, 'left', { rank: 501 });
    // Add command
    commands.addCommand(CommandIDs.slurmUI, {
        label: (args) => ('Go to slurm wrapper'),
        caption: 'Go to slurm wrapper',
        icon: (args) => _icon__WEBPACK_IMPORTED_MODULE_3__.slurmelIcon,
        execute: () => {
            try {
                shell.activateById('slurm-wrapper-widget');
            }
            catch (err) {
                console.error('Fail to open Slurm Wrapper tab.');
            }
        }
    });
    commands.addCommand(CommandIDs.dialog, {
        label: (args) => ('Configure slurm wrapper'),
        caption: 'Configure slurm wrapper',
        icon: (args) => _icon__WEBPACK_IMPORTED_MODULE_3__.slurmelIcon,
        execute: async () => {
            const config_system = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.sendGetRequest)();
            const buttons = [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: 'Cancel' }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Save' })
            ];
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: (0,_kernelSelector__WEBPACK_IMPORTED_MODULE_5__.getTitle)(config_system.documentationhref),
                body: new _widgets__WEBPACK_IMPORTED_MODULE_2__.SlurmConfigWidget(config_system, available_kernel_names),
                buttons: buttons
            }).then((e) => {
                (0,_kernelSelector__WEBPACK_IMPORTED_MODULE_5__.handleResult)(e, null);
                slurmPanel.update();
            });
        }
    });
    const x = true;
    // Add to Palette
    if (palette && x) {
        [CommandIDs.slurmUI, CommandIDs.dialog].forEach((command) => {
            palette.addItem({ command, category, args: { 'isPalette': true } });
        });
    }
    // Add WidgetExtension to Notebook (Toolbar Countdown)
    app.docRegistry.addWidgetExtension('Notebook', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.ToolbarCountdown());
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/kernelSelector.js":
/*!*******************************!*\
  !*** ./lib/kernelSelector.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DialogCustom": () => (/* binding */ DialogCustom),
/* harmony export */   "createKernelNameItemCustom": () => (/* binding */ createKernelNameItemCustom),
/* harmony export */   "getBody": () => (/* binding */ getBody),
/* harmony export */   "getTitle": () => (/* binding */ getTitle),
/* harmony export */   "handleResult": () => (/* binding */ handleResult)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widgets */ "./lib/widgets.js");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");







// import { slurmelIcon2 } from './icon';
function getTitle(documentationhref) {
    const spanOutStyle = {
        display: "flex",
        width: "100%",
        justifyContent: "space-between"
    };
    const aStyle = {
        color: "#1a0dab",
        textDecoration: "underline"
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: spanOutStyle },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, "Configure Slurm Wrapper"),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { style: aStyle, href: documentationhref, target: '_blank' }, "Documentation")));
}
async function getBody(config_system, available_kernels) {
    let available_kernel_names = {};
    for (let key in available_kernels) {
        let kernel = available_kernels[key];
        try {
            if (kernel.metadata["kernel_provisioner"]["provisioner_name"] != "slurm-provisioner") {
                available_kernel_names[kernel.display_name] = kernel.argv;
            }
        }
        catch (error) {
            available_kernel_names[kernel.display_name] = kernel.argv;
        }
    }
    const body = new _widgets__WEBPACK_IMPORTED_MODULE_3__.SlurmConfigWidget(config_system, available_kernel_names);
    return body;
}
async function handleResult(result, sessionContext) {
    const model = result.value;
    if (model && (result.button.accept || result.button.save)) {
        await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.sendPostRequest)(model);
    }
    if (sessionContext) {
        if (sessionContext.isDisposed || !result.button.accept) {
            return;
        }
        let previous_name = '';
        if (sessionContext._session) {
            previous_name = sessionContext._session._kernel._name;
        }
        if (model && previous_name != "slurm-provisioner-kernel") {
            await sessionContext.changeKernel(model);
        }
    }
}
function saveButton(options = {}) {
    options.save = true;
    return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton(options);
}
class DialogCustom {
    async selectKernel(sessionContext, translator) {
        var _b;
        if (sessionContext.isDisposed) {
            return Promise.resolve();
        }
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        // If there is no existing kernel, offer the option
        // to keep no kernel.
        let label = trans.__('Cancel');
        if (sessionContext.hasNoKernel) {
            label = sessionContext.kernelDisplayName;
        }
        const buttons = [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label }),
            saveButton({ label: "Save" }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('(Re)Start') })
        ];
        // Load available kernels, excecpt the slurm one, in a list
        const config_system = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.sendGetRequest)();
        const body = await getBody(config_system, (_b = sessionContext.specsManager.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs);
        const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog({
            title: getTitle(config_system.documentationhref),
            body: body,
            buttons
        });
        const result = await dialog.launch();
        await handleResult(result, sessionContext);
    }
    async restart(sessionContext, translator) {
        var _a;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        await sessionContext.initialize();
        if (sessionContext.isDisposed) {
            throw new Error('session already disposed');
        }
        const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel && sessionContext.prevKernelName) {
            await sessionContext.changeKernel({
                name: sessionContext.prevKernelName
            });
            return true;
        }
        // Bail if there is no previous kernel to start.
        if (!kernel) {
            throw new Error('No kernel to restart');
        }
        const restartBtn = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: 'Restart' });
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Restart Kernel?'),
            body: trans.__('Do you want to restart the current kernel? All variables will be lost.'),
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), restartBtn]
        });
        if (kernel.isDisposed) {
            return false;
        }
        if (result.button.accept) {
            await sessionContext.restartKernel();
            return true;
        }
        return false;
    }
}
function KernelNameComponentCustom(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    // const trans = translator.load('jupyterlab');
    const callback = () => {
        void props.dialogs.selectKernel(props.sessionContext, translator);
    };
    const TOOLBAR_KERNEL_NAME_CLASS = 'jp-Toolbar-kernelName';
    const label = "Configure Slurm Wrapper";
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.UseSignal, { signal: props.sessionContext.kernelChanged, initialSender: props.sessionContext }, sessionContext => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButtonComponent, { className: TOOLBAR_KERNEL_NAME_CLASS, onClick: callback, 
        // tooltip={trans.__('Configure wrapper')}
        label: label, icon: _icon__WEBPACK_IMPORTED_MODULE_5__.slurmelIcon2 }))));
}
function createKernelNameItemCustom(sessionContext, dialogs, translator) {
    const el = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_0__.createElement(KernelNameComponentCustom, { sessionContext: sessionContext, dialogs: dialogs !== null && dialogs !== void 0 ? dialogs : _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs, translator: translator }));
    el.addClass('jp-KernelName');
    return el;
}


/***/ }),

/***/ "./lib/toolbar.js":
/*!************************!*\
  !*** ./lib/toolbar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ToolbarCountdown": () => (/* binding */ ToolbarCountdown)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets */ "./lib/widgets.js");
/* harmony import */ var _kernelSelector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./kernelSelector */ "./lib/kernelSelector.js");






class ToolbarCountdown {
    /**
     * Create a new extension for the notebook panel widget.
     *
     * @param panel Notebook panel
     * @param context Notebook context
     * @returns Disposable on the added button
     */
    createNew(panel, context) {
        const countdown = new KernelCountdownWidget(panel);
        const x = (0,_kernelSelector__WEBPACK_IMPORTED_MODULE_3__.createKernelNameItemCustom)(panel.sessionContext, new _kernelSelector__WEBPACK_IMPORTED_MODULE_3__.DialogCustom());
        panel.toolbar.insertItem(11, 'Slurmel', x);
        panel.toolbar.insertItem(11, 'Countdown', countdown);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            x.dispose();
            countdown.dispose();
        });
    }
}
class KernelCountdownWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(panel) {
        super();
        this.panel = panel;
    }
    render() {
        let x = react__WEBPACK_IMPORTED_MODULE_1__.createElement(RemainingTimeComp, { panel: this.panel });
        return x;
    }
}
class RemainingTimeComp extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    constructor(props) {
        super(props);
        this.state = {
            date_show: false,
            date_endtime: 0,
            date_label: "Remaining time: "
        };
        this.props.panel.sessionContext.kernelChanged.connect(this._kernelChanged, this);
    }
    async _kernelChanged(a, b) {
        let found_kernel = false;
        if (b.newValue) {
            const kernelID = b.newValue._id;
            const config_system = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.sendGetRequest)();
            for (let x in config_system.allocations) {
                if ((!found_kernel) && config_system.allocations[x].kernel_ids.includes(kernelID)) {
                    this.setState({
                        date_endtime: config_system.allocations[x].endtime,
                        date_show: true,
                        date_label: "Remaining time ( allocation " + String(x) + " ): "
                    });
                    found_kernel = true;
                }
            }
            /**
             * Request - get current slurm_provisioner.json
             * Run through all allocations, find kernel_id in list
             * If there -> show allocID + endtime (tickDown)
             * If not there -> show nothing
             */
        }
        this.setState({ date_show: found_kernel });
    }
    render() {
        const timer = react__WEBPACK_IMPORTED_MODULE_1__.createElement(_widgets__WEBPACK_IMPORTED_MODULE_5__.AllocationTimer, { key_: "timer", date_label: this.state.date_label, date_endtime: this.state.date_endtime });
        const style = {
            alignSelf: "center"
        };
        if (this.state.date_show) {
            return react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { style: style }, timer);
        }
        else {
            return null;
        }
    }
}


/***/ }),

/***/ "./lib/widgets.js":
/*!************************!*\
  !*** ./lib/widgets.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AllocationTimer": () => (/* binding */ AllocationTimer),
/* harmony export */   "CurrentSlurmConfig": () => (/* binding */ CurrentSlurmConfig),
/* harmony export */   "SlurmConfigWidget": () => (/* binding */ SlurmConfigWidget),
/* harmony export */   "SlurmConfigurator": () => (/* binding */ SlurmConfigurator),
/* harmony export */   "SlurmPanel": () => (/* binding */ SlurmPanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");





;
const labelClass = 'slurm-input-label';
const spanClass = 'slurm-config-span';
class SlurmPanel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(commands, available_kernel_names) {
        super();
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this.id = 'slurm-wrapper-widget';
        this.addClass('slurm-wrapper-panel');
        this.title.icon = _icon__WEBPACK_IMPORTED_MODULE_3__.slurmelIcon;
        this.title.caption = 'Slurm Wrapper';
        this._commands = commands;
    }
    get stateChanged() {
        return this._stateChanged;
    }
    async onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        // Emit change upon update
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.sendGetRequest)();
        this._stateChanged.emit(data);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("h2", null, "Current Configuration"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(CurrentSlurmConfig, { panel: this }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(SlurmConfigurator, { commands: this._commands })));
    }
}
/**
 * Slurm configurator widget
 */
class SlurmConfigWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(config_system, available_kernels) {
        super();
        this._available_kernels = available_kernels;
        this._config_system = config_system;
        this.slurmelRef = react__WEBPACK_IMPORTED_MODULE_0__.createRef();
    }
    getValue() {
        // Collect selected config to update slurm-provisioner-kernel
        const state = this.slurmelRef.current.state;
        const kernel = state.kernel;
        const kernel_argv = this._available_kernels[state.kernel][1];
        const kernel_language = this._available_kernels[state.kernel][2];
        let allocation = "";
        let node = "";
        if (state.allocation === "New") {
            allocation = "None";
        }
        else {
            allocation = state.allocation;
        }
        if (state.allocation_node === "Any") {
            node = "None";
        }
        else {
            node = state.allocation_node;
        }
        const config = {
            allocation,
            node,
            kernel,
            kernel_argv,
            kernel_language,
            project: state.project,
            partition: state.partition,
            nodes: state.nodes,
            gpus: state.gpus,
            runtime: state.runtime,
            name: "slurm-provisioner-kernel"
        };
        return config;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(SlurmelComponents, { available_kernels: this._available_kernels, config_system: this._config_system, ref: this.slurmelRef }));
    }
}
/**
 * Contains all elements and logic for the kernel configurator.
 * Only called by SlurmWidget in this file.
 */
class SlurmelComponents extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        // bind onClick / onChange functions
        this.handleDropdownChange = this.handleDropdownChange.bind(this);
        this.handleAllocationChange = this.handleAllocationChange.bind(this);
        this.handleNodeChange = this.handleNodeChange.bind(this);
        this.handleKernelChange = this.handleKernelChange.bind(this);
        this.handleNumberChange = this.handleNumberChange.bind(this);
        // translate current_config from kernel.json to this state
        const current_config_comp = this.get_current_config(props.config_system.current_config);
        // apply default values
        this.state = this.default_values(props, current_config_comp);
    }
    get_current_config(current_config) {
        let allocation = current_config.jobid || "None";
        let allocation_node = current_config.node || "None";
        if (allocation === "None") {
            allocation = "";
            allocation_node = "";
        }
        else {
            if (allocation_node === "None") {
                allocation_node = "";
            }
        }
        let kernel = current_config.kernel || "";
        let project = current_config.project || "";
        let partition = current_config.partition || "";
        let nodes = current_config.nodes || "";
        let gpus = current_config.gpus || "";
        let runtime = current_config.runtime || "";
        let reservation = current_config.runtime || "";
        return ({
            allocation,
            allocation_node,
            kernel,
            project,
            partition,
            nodes,
            gpus,
            runtime,
            reservation,
        });
    }
    default_values(props, { resources_editable = true, project = "", partition = "", nodes = "", gpus = "", runtime = "", reservation = "", allocation = "", kernel = "", date_show = false, date_endtime = "", allocation_node = "" } = {}) {
        // setup some default values
        const dl = props.config_system.dropdown_lists;
        let tmp = dl.projects;
        if (project === "") {
            project = tmp.length > 0 ? tmp[0] : "";
        }
        const projects = tmp.includes(project) ? tmp : [project];
        tmp = dl.partitions[project];
        if (partition === "") {
            partition = tmp && tmp.length > 0 ? tmp[0] : "";
        }
        const partitions = tmp && tmp.includes(partition) ? tmp : [partition];
        const partition_config = props.config_system.resources[partition];
        if (nodes === "") {
            nodes = partition_config && partition_config.nodes ? partition_config.nodes.default : "0";
        }
        const nodes_min = partition_config && partition_config.nodes ? partition_config.nodes.minmax[0] : "0";
        const nodes_max = partition_config && partition_config.nodes ? partition_config.nodes.minmax[1] : "0";
        if (gpus === "") {
            gpus = partition_config && partition_config.gpus ? partition_config.gpus.default : "0";
        }
        const gpus_min = partition_config && partition_config.gpus ? partition_config.gpus.minmax[0] : "0";
        const gpus_max = partition_config && partition_config.gpus ? partition_config.gpus.minmax[1] : "0";
        if (runtime === "") {
            runtime = partition_config && partition_config.runtime ? partition_config.runtime.default : "0";
        }
        const runtime_min = partition_config && partition_config.runtime ? partition_config.runtime.minmax[0] : "0";
        const runtime_max = partition_config && partition_config.runtime ? partition_config.runtime.minmax[1] : "0";
        if (reservation === "") {
            reservation = "None";
        }
        tmp = dl.reservations;
        const reservations = project in tmp && partition in dl.reservations[project] ? dl.reservations[project][partition] : ["None"];
        console.log(props.config_system.allocations);
        if (allocation === "" || !(props.config_system.allocations.hasOwnProperty(allocation))) {
            allocation = "New";
        }
        let allocation_names = ["New"];
        for (let key in props.config_system.allocations) {
            allocation_names.push(key);
        }
        // Node where to start the kernel on
        if (allocation_node === "") {
            allocation_node = "Any";
        }
        let allocation_node_names = ["Any"];
        if (allocation != "New") {
            let tmp = props.config_system.allocations[allocation];
            if (tmp.nodelist) {
                allocation_node_names = allocation_node_names.concat(tmp.nodelist);
            }
        }
        // Kernels the user wants to start
        let kernel_names = [];
        for (let key in props.available_kernels) {
            kernel_names.push(key);
        }
        if (kernel === "") {
            kernel = String(kernel_names[0]);
        }
        // show rest time for allocation
        if (allocation === "New") {
            date_show = false;
            resources_editable = true;
        }
        else {
            date_show = true;
            resources_editable = false;
        }
        if (date_show && date_endtime == "") {
            let tmp = props.config_system.allocations[allocation];
            date_endtime = tmp.endtime;
        }
        return ({
            resources_editable,
            project,
            projects,
            partition,
            partitions,
            nodes,
            nodes_min,
            nodes_max,
            gpus,
            gpus_min,
            gpus_max,
            runtime,
            runtime_min,
            runtime_max,
            reservation,
            reservations,
            kernel,
            kernel_names,
            allocation,
            allocation_names,
            date_show,
            date_endtime,
            allocation_node,
            allocation_node_names
        });
    }
    handleAllocationChange(key, value) {
        if (value == "New") {
            if (this.state.allocation != value) {
                // do not change kernel, but anything else to default
                this.setState(this.default_values(this.props, { kernel: this.state.kernel }));
            }
        }
        else {
            // Pre existing allocation. Do not allow changes to resources and set them to
            // previous used values
            const config = this.props.config_system.allocations[value].config;
            const project = config.project;
            const partition = config.partition;
            const gpus = config.gpus ? config.gpus : "";
            const nodes = config.nodes ? config.nodes : "";
            const runtime = config.runtime ? config.runtime : "";
            const reservation = config.reservation;
            const date_endtime = this.props.config_system.allocations[value].endtime;
            this.setState(this.default_values(this.props, {
                resources_editable: false,
                project,
                partition,
                nodes,
                gpus,
                runtime,
                reservation,
                allocation: value,
                allocation_node: "Any",
                kernel: this.state.kernel,
                date_show: true,
                date_endtime
            }));
        }
    }
    handleNodeChange(key, allocation_node) {
        this.setState({ allocation_node });
    }
    handleKernelChange(key, kernel) {
        this.setState({ kernel });
    }
    /**
     * Handle changes in all Dropdown menus
     * @param key key of the dropdown which has changed
     * @param value new value
     */
    handleDropdownChange(key, value) {
        // this.state.key will be updated after this function. So we have to track
        // new actual new values manually.
        const dl = this.props.config_system.dropdown_lists;
        let project = this.state.project;
        let partition = this.state.partition;
        if (key === "partitions") {
            partition = value;
            // Update the chosen partition
            this.setState({ partition });
        }
        else if (key === "projects") {
            project = value;
            // Update the chosen project
            this.setState({ project });
            const partitions = dl.partitions[project];
            partition = partitions[0];
            // Update the partition dropdown menu
            this.setState({
                partition,
                partitions
            });
        }
        if (key === "reservations") {
            // Update selected reservation
            this.setState({ reservation: value });
        }
        else {
            // Update Resources, this will update nodes, gpus, runtime and reservation while keeping the given parameters
            this.setState(this.default_values(this.props, {
                project,
                partition,
                allocation: this.state.allocation,
                kernel: this.state.kernel,
                date_show: this.state.date_show,
                date_endtime: this.state.date_endtime
            }));
        }
    }
    /**
     * Checks if new value for number-input field is valide
     * @param value new value for input field
     * @returns
     */
    validateNumber(value) {
        try {
            if (isNaN(parseInt(value))) {
                console.log("Only positive numbers are allowed in nodes field.");
                return false;
            }
            else if (value.includes(".")) {
                console.log("Only positive numbers are allowed in nodes field.");
                return false;
            }
        }
        catch (e) {
            console.log("Only positive numbers are allowed in nodes field.");
            return false;
        }
        return true;
    }
    /**
     * Handle changes in all number-input fields
     * @param key key of the input field which has changed
     * @param value new value
     */
    handleNumberChange(key, value) {
        // if ( ! this.validateNumber(value) ) {
        //   return;
        // }
        const partition = this.state.partition;
        let max = "0";
        if (key === "runtime") {
            max = this.props.config_system.resources[partition].runtime.minmax[1];
        }
        else if (key == "nodes") {
            max = this.props.config_system.resources[partition].nodes.minmax[1];
        }
        else if (key == "gpus") {
            max = this.props.config_system.resources[partition].gpus.minmax[1];
        }
        else {
            console.log("Unsupported key: " + key);
            return;
        }
        if (parseInt(value) > parseInt(max)) {
            value = max.toString();
        }
        this.setState({
            [key]: value
        });
    }
    /**
     * Renders all components for the slurm configurator widget
     * @returns JSX.Element containing all html elements + logic
     */
    render() {
        const allocations = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select allocation for slurm wrapper", key_: "allocations", selected: this.state.allocation, values: this.state.allocation_names, onValueChange: this.handleAllocationChange, editable: true, available_kernels: {} });
        const allocnodes = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select node for slurm wrapper", key_: "allocations_nodes", selected: this.state.allocation_node, values: this.state.allocation_node_names, onValueChange: this.handleNodeChange, editable: true, available_kernels: {} });
        const kernels = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select kernel for slurm wrapper", key_: "kernels", selected: this.state.kernel, values: this.state.kernel_names, onValueChange: this.handleKernelChange, editable: true, available_kernels: this.props.available_kernels });
        const projects = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select project for slurm wrapper", key_: "projects", selected: this.state.project, values: this.state.projects, onValueChange: this.handleDropdownChange, editable: this.state.resources_editable, available_kernels: {} });
        const partitions = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select partition for slurm wrapper", key_: "partitions", selected: this.state.partition, values: this.state.partitions, onValueChange: this.handleDropdownChange, editable: this.state.resources_editable, available_kernels: {} });
        const reservations = react__WEBPACK_IMPORTED_MODULE_0__.createElement(DropdownComponent, { label: "Select reservation for slurm wrapper", key_: "reservations", selected: this.state.reservation, values: this.state.reservations, onValueChange: this.handleDropdownChange, editable: this.state.resources_editable, available_kernels: {} });
        const nodes = react__WEBPACK_IMPORTED_MODULE_0__.createElement(InputNumberComponent, { label: "Nodes", key_: "nodes", value: this.state.nodes, min: this.state.nodes_min, max: this.state.nodes_max, onValueChange: this.handleNumberChange, editable: this.state.resources_editable });
        const gpus = react__WEBPACK_IMPORTED_MODULE_0__.createElement(InputNumberComponent, { label: "GPUs", key_: "gpus", value: this.state.gpus, min: this.state.gpus_min, max: this.state.gpus_max, onValueChange: this.handleNumberChange, editable: this.state.resources_editable });
        const runtime = react__WEBPACK_IMPORTED_MODULE_0__.createElement(InputNumberComponent, { label: "Runtime (min)", key_: "runtime", value: this.state.runtime, min: this.state.runtime_min, max: this.state.runtime_max, onValueChange: this.handleNumberChange, editable: this.state.resources_editable });
        const timer = react__WEBPACK_IMPORTED_MODULE_0__.createElement(AllocationTimer, { key_: "timer", date_label: "Time left: ", date_endtime: this.state.date_endtime });
        const divStyle = {
            minWidth: '450px',
            overflow: 'auto'
        };
        if (this.state.allocation == "New") {
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: divStyle },
                allocations,
                allocnodes,
                kernels,
                projects,
                partitions,
                nodes,
                gpus,
                runtime,
                reservations));
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: divStyle },
                allocations,
                allocnodes,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Kernel", value: this.state.kernel }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Project", value: this.state.project }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Partition", value: this.state.partition }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Nodes", value: this.state.nodes }),
                this.state.gpus > 0 && react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "GPUs", value: this.state.gpus }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Runtime", value: this.state.runtime }),
                this.state.reservations.length < 2 && react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Reservation", value: this.state.reservation }),
                this.state.date_show && timer));
        }
    }
}
/**
 * Component containing info about current slurm configuration.
 */
class CurrentSlurmConfig extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.props.panel.stateChanged.connect(this._updateState, this);
        this.state = {
            empty: false,
            allocation: '',
            node: '',
            kernel: '',
            project: '',
            partition: '',
            nodes: '',
            gpus: '',
            runtime: '',
            reservation: '',
            endtime: '',
        };
    }
    _updateState(emitter, data) {
        console.log(data);
        const current_config = data.current_config;
        if (Object.keys(current_config).length === 0) {
            // Nothing configured yet.
            this.setState({
                empty: true,
            });
        }
        else {
            let allocation = current_config.jobid;
            let node = current_config.node;
            if (allocation == "None")
                allocation = "New";
            if (node == "None")
                node = "Any";
            // Save configuration to state.
            this.setState({
                empty: false,
                allocation: allocation,
                node: node,
                kernel: current_config.kernel,
                project: current_config.project,
                partition: current_config.partition,
                nodes: current_config.nodes,
                gpus: current_config.gpus,
                runtime: current_config.runtime,
                reservation: current_config.reservation,
            });
            // Save endtime if exists.
            let jobid = current_config.jobid;
            if (data.allocations[jobid]) {
                this.setState({
                    endtime: data.allocations[jobid].endtime,
                });
            }
        }
    }
    render() {
        // Nothing configured yet.
        if (this.state.empty) {
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null, "Nothing configured yet. Click configure and choose a partition."));
        }
        // Return current configuration.
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Allocation", value: this.state.allocation }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Node", value: this.state.node }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Kernel", value: this.state.kernel }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Project", value: this.state.project }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Partition", value: this.state.partition }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Nodes", value: this.state.nodes }),
            this.state.gpus != "0" && react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "GPUs", value: this.state.gpus }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Runtime", value: this.state.runtime }),
            this.state.reservation != "None" &&
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(InfoComponent, { label: "Reservation", value: this.state.reservation }),
            this.state.endtime && react__WEBPACK_IMPORTED_MODULE_0__.createElement(AllocationTimer, { key_: "timer", date_label: "Time left: ", date_endtime: this.state.endtime })));
    }
}
/**
 * Component containing button opening the slurm configuration dialog.
 */
class SlurmConfigurator extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "slurm-config-btn", onClick: () => this.props.commands.execute('open-slurm-config-dialog') }, "Configure")));
    }
}
class AllocationTimer extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = this.get_time_values();
    }
    componentDidMount() {
        this._timerID = setInterval(() => this.tick(), 1000);
    }
    componentWillUnmount() {
        clearInterval(this._timerID);
    }
    get_time_values() {
        const now = Math.floor(new Date().getTime() / 1000);
        // Find the distance between now and the count down date
        const distance = Math.floor(this.props.date_endtime / 1) - now;
        // Time calculations for days, hours, minutes and seconds
        const hours = String(Math.floor((distance % (60 * 60 * 24)) / (60 * 60)));
        const minutes = String(Math.floor((distance % (60 * 60)) / (60)));
        const seconds = String(Math.floor((distance % (60))));
        return {
            distance: String(distance),
            hours,
            minutes,
            seconds
        };
    }
    tick() {
        this.setState(this.get_time_values());
    }
    render() {
        let spanStyle = { color: 'var(--jp-ui-font-color0)' };
        if (parseInt(this.state.distance) < 300) {
            spanStyle.color = 'var(--jp-error-color1)';
        }
        const minutes_ = "0" + this.state.minutes;
        const minutes = minutes_.substring(minutes_.length - 2);
        const seconds_ = "0" + this.state.seconds;
        const seconds = seconds_.substring(seconds_.length - 2);
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'lm-Widget p-Widget jp-Dialog-body' },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("label", { className: labelClass },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: spanClass, style: spanStyle },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { fontWeight: 'bold' } }, this.props.date_label),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { float: 'right' } },
                        this.state.hours,
                        ":",
                        minutes,
                        ":",
                        seconds)))));
    }
}
/**
 * Component class for all <select> elements
 */
class DropdownComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        this.props.onValueChange(this.props.key_, e.target.value);
    }
    render() {
        if (this.props.key_ === "reservations" && this.props.values.length < 2) {
            // If there's only "None" as reservation we don't have to show it.
            return null;
        }
        const selected = this.props.selected;
        const values = this.props.values;
        let valuesReact = {};
        if (this.props.key_ === "kernels") {
            valuesReact = values.map(x => {
                if (x === selected) {
                    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: x, selected: true }, this.props.available_kernels[x][0]);
                }
                else {
                    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: x }, this.props.available_kernels[x][0]);
                }
            });
        }
        else {
            valuesReact = values.map(x => {
                if (x === selected) {
                    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { selected: true }, x);
                }
                else {
                    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", null, x);
                }
            });
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'lm-Widget p-Widget jp-Dialog-body' },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("label", null,
                this.props.label,
                " :"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'jp-select-wrapper' },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("select", { className: 'slurmel-select', key: this.props.key_, disabled: !this.props.editable, name: this.props.key_, onChange: this.handleChange }, valuesReact))));
    }
}
/**
 * Component class for all <input type="number"> elements
 */
// class InputNumberComponent extends React.Component<INumberInputProps, ISlurmComponentState> {
class InputNumberComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        this.props.onValueChange(this.props.key_, e.target.value);
    }
    render() {
        let inputClasses = 'jp-mod-styled slurmel-input';
        if (!this.props.editable)
            inputClasses += ' disabled';
        if (this.props.key_ === "gpus" && this.props.value === "0") {
            return null;
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'lm-Widget p-Widget jp-Dialog-body' },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("label", { className: labelClass },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: spanClass },
                    this.props.label,
                    " [",
                    this.props.min,
                    "-",
                    this.props.max,
                    "]:"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("input", { className: inputClasses, type: "number", disabled: !this.props.editable, key: this.props.key_, id: this.props.key_, name: this.props.key_, value: this.props.value, min: this.props.min, max: this.props.max, onChange: this.handleChange }))));
    }
}
/**
 * Component class for displaying configuration info components
 */
class InfoComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { fontWeight: 'bold' } },
                this.props.label,
                ":"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { float: 'right' } }, this.props.value)));
    }
}


/***/ }),

/***/ "./style/slurmel-icon-notebook.svg":
/*!*****************************************!*\
  !*** ./style/slurmel-icon-notebook.svg ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg\n   width=\"40.000004\"\n   height=\"40\"\n   viewBox=\"0 0 10.583334 10.583334\"\n   version=\"1.1\"\n   id=\"svg873\"\n   inkscape:version=\"1.1.2 (b8e25be833, 2022-02-05)\"\n   sodipodi:docname=\"drawing.svg\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <sodipodi:namedview\n     id=\"namedview875\"\n     pagecolor=\"#ffffff\"\n     bordercolor=\"#666666\"\n     borderopacity=\"1.0\"\n     inkscape:pageshadow=\"2\"\n     inkscape:pageopacity=\"0.0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:document-units=\"mm\"\n     showgrid=\"false\"\n     fit-margin-top=\"0\"\n     fit-margin-left=\"0\"\n     fit-margin-right=\"0\"\n     fit-margin-bottom=\"0\"\n     units=\"px\"\n     inkscape:zoom=\"0.76435185\"\n     inkscape:cx=\"-8.503937\"\n     inkscape:cy=\"202.13204\"\n     inkscape:window-width=\"1920\"\n     inkscape:window-height=\"1051\"\n     inkscape:window-x=\"-9\"\n     inkscape:window-y=\"-9\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"layer1\" />\n  <defs\n     id=\"defs870\">\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient4679\"\n       id=\"linearGradient1468\"\n       gradientUnits=\"userSpaceOnUse\"\n       gradientTransform=\"matrix(1.7201279,0,0,1.7367347,-45.8396,-35.783308)\"\n       x1=\"26.648937\"\n       y1=\"20.603781\"\n       x2=\"135.66525\"\n       y2=\"114.39767\" />\n    <linearGradient\n       id=\"linearGradient4679\">\n      <stop\n         style=\"stop-color:#5a9fd4;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop4681\" />\n      <stop\n         style=\"stop-color:#306998;stop-opacity:1;\"\n         offset=\"1\"\n         id=\"stop4683\" />\n    </linearGradient>\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient4661\"\n       id=\"linearGradient1465\"\n       gradientUnits=\"userSpaceOnUse\"\n       gradientTransform=\"matrix(1.7166332,0,0,1.7332063,65.036885,71.326052)\"\n       x1=\"150.96111\"\n       y1=\"192.35176\"\n       x2=\"112.03144\"\n       y2=\"137.27299\" />\n    <linearGradient\n       id=\"linearGradient4661\">\n      <stop\n         style=\"stop-color:#ffd43b;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop4663\" />\n      <stop\n         style=\"stop-color:#ffe873;stop-opacity:1\"\n         offset=\"1\"\n         id=\"stop4665\" />\n    </linearGradient>\n  </defs>\n  <g\n     inkscape:label=\"Layer 1\"\n     inkscape:groupmode=\"layer\"\n     id=\"layer1\"\n     transform=\"translate(-107.20833,-95.092954)\">\n    <g\n       id=\"g1411\"\n       transform=\"matrix(0.02351852,0,0,0.02351852,107.20833,95.092954)\">\n      <path\n         fill=\"#42afeb\"\n         d=\"m 217.79209,173.05964 c -3.91294,0 -7.08401,3.14839 -7.08401,7.03332 v 0 13.53739 c 0,3.8822 3.17107,7.03436 7.08401,7.03436 v 0 h 14.07039 c 3.91295,0 7.08917,-3.15216 7.08917,-7.03436 v 0 -13.53739 c 0,-3.88493 -3.17622,-7.03332 -7.08917,-7.03332 v 0 z m 34.58434,21.41998 c -2.93919,0 -5.32283,2.4077 -5.32283,5.36973 v 0 10.33007 c 0,2.96509 2.38364,5.3711 5.32283,5.3711 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40601 5.32111,-5.3711 v 0 -10.33007 c 0,-2.96203 -2.38158,-5.36973 -5.32111,-5.36973 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.4077 -5.32216,5.36973 v 0 10.33007 c 0,2.96509 2.38399,5.3711 5.32216,5.3711 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40601 5.32283,-5.3711 v 0 -10.33007 c 0,-2.96203 -2.38502,-5.36973 -5.32283,-5.36973 v 0 z m 31.08578,11.84875 c -3.91294,0 -7.08401,3.14668 -7.08401,7.03403 v 0 13.53634 c 0,3.88425 3.17107,7.03538 7.08401,7.03538 v 0 h 14.07039 c 3.91295,0 7.08917,-3.15113 7.08917,-7.03538 v 0 -13.53634 c 0,-3.88735 -3.17622,-7.03403 -7.08917,-7.03403 v 0 z m 61.77894,6.3461 c -2.18592,0 -3.95779,1.78763 -3.95779,3.99527 v 0 7.6846 c 0,2.20284 1.77187,3.99184 3.95779,3.99184 v 0 h 7.86453 c 2.18456,0 3.9578,-1.789 3.9578,-3.99184 v 0 -7.6846 c 0,-2.20764 -1.77324,-3.99527 -3.9578,-3.99527 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.78763 -3.95919,3.99527 v 0 7.6846 c 0,2.20284 1.77391,3.99184 3.95919,3.99184 v 0 h 7.86208 c 2.18802,0 3.95987,-1.789 3.95987,-3.99184 v 0 -7.6846 c 0,-2.20764 -1.77185,-3.99527 -3.95987,-3.99527 v 0 z m 89.81026,8.08783 c -2.93919,0 -5.32283,2.40394 -5.32283,5.3663 v 0 10.33349 c 0,2.96271 2.38364,5.36766 5.32283,5.36766 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40495 5.32111,-5.36766 v 0 -10.33349 c 0,-2.96236 -2.38158,-5.3663 -5.32111,-5.3663 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.40394 -5.32216,5.3663 v 0 10.33349 c 0,2.96271 2.38399,5.36766 5.32216,5.36766 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40495 5.32283,-5.36766 v 0 -10.33349 c 0,-2.96236 -2.38502,-5.3663 -5.32283,-5.3663 v 0 z m 92.86472,13.01732 c -2.18592,0 -3.95779,1.78659 -3.95779,3.99149 v 0 7.68494 c 0,2.20319 1.77187,3.99252 3.95779,3.99252 v 0 h 7.86453 c 2.18456,0 3.9578,-1.78933 3.9578,-3.99252 v 0 -7.68494 c 0,-2.2049 -1.77324,-3.99149 -3.9578,-3.99149 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.78659 -3.95919,3.99149 v 0 7.68494 c 0,2.20319 1.77391,3.99252 3.95919,3.99252 v 0 h 7.86208 c 2.18802,0 3.95987,-1.78933 3.95987,-3.99252 v 0 -7.68494 c 0,-2.2049 -1.77185,-3.99149 -3.95987,-3.99149 v 0 z m 55.22592,5.528 c -3.91294,0 -7.08401,3.14975 -7.08401,7.03505 v 0 13.53736 c 0,3.88462 3.17107,7.03199 7.08401,7.03199 v 0 h 14.07039 c 3.91295,0 7.08917,-3.14737 7.08917,-7.03199 v 0 -13.53736 c 0,-3.8853 -3.17622,-7.03505 -7.08917,-7.03505 v 0 z m 85.02057,5.78359 c -1.62555,0 -2.94057,1.32854 -2.94057,2.96508 v 0 5.70443 c 0,1.63654 1.31502,2.96272 2.94057,2.96272 v 0 H 308.65 c 1.62072,0 2.93469,-1.32618 2.93469,-2.96272 v 0 -5.70443 c 0,-1.63654 -1.31397,-2.96508 -2.93469,-2.96508 v 0 z m -161.45955,0 c -1.62317,0 -2.93816,1.32854 -2.93816,2.96508 v 0 5.70443 c 0,1.63654 1.31499,2.96272 2.93816,2.96272 v 0 h 5.83491 c 1.62418,0 2.93885,-1.32618 2.93885,-2.96272 v 0 -5.70443 c 0,-1.63654 -1.31467,-2.96508 -2.93885,-2.96508 v 0 z m 111.02332,1.95856 c -2.93919,0 -5.32283,2.40223 -5.32283,5.36527 v 0 10.33144 c 0,2.96509 2.38364,5.36938 5.32283,5.36938 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40429 5.32111,-5.36938 v 0 -10.33144 c 0,-2.96304 -2.38158,-5.36527 -5.32111,-5.36527 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.40223 -5.32216,5.36527 v 0 10.33144 c 0,2.96509 2.38399,5.36938 5.32216,5.36938 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40429 5.32283,-5.36938 v 0 -10.33144 c 0,-2.96304 -2.38502,-5.36527 -5.32283,-5.36527 v 0 z m 92.86472,7.99259 c -2.18592,0 -3.95779,1.79139 -3.95779,3.99834 v 0 7.68288 c 0,2.20729 1.77187,3.99184 3.95779,3.99184 v 0 h 7.86453 c 2.18456,0 3.9578,-1.78455 3.9578,-3.99184 v 0 -7.68288 c 0,-2.20695 -1.77324,-3.99834 -3.9578,-3.99834 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.79139 -3.95919,3.99834 v 0 7.68288 c 0,2.20729 1.77391,3.99184 3.95919,3.99184 v 0 h 7.86208 c 2.18802,0 3.95987,-1.78455 3.95987,-3.99184 v 0 -7.68288 c 0,-2.20695 -1.77185,-3.99834 -3.95987,-3.99834 v 0 z m 140.24649,7.42285 c -1.62555,0 -2.94057,1.3272 -2.94057,2.96374 v 0 5.70443 c 0,1.63346 1.31502,2.9651 2.94057,2.9651 v 0 H 308.65 c 1.62072,0 2.93469,-1.33164 2.93469,-2.9651 v 0 -5.70443 c 0,-1.63654 -1.31397,-2.96374 -2.93469,-2.96374 v 0 z m -161.45955,0 c -1.62317,0 -2.93816,1.3272 -2.93816,2.96374 v 0 5.70443 c 0,1.63346 1.31499,2.9651 2.93816,2.9651 v 0 h 5.83491 c 1.62418,0 2.93885,-1.33164 2.93885,-2.9651 v 0 -5.70443 c 0,-1.63654 -1.31467,-2.96374 -2.93885,-2.96374 v 0 z m 180.73096,5.69999 c -1.22528,0 -2.22078,1.00103 -2.22078,2.23642 v 0 4.30358 c 0,1.23161 0.9955,2.23471 2.22078,2.23471 v 0 h 4.40293 c 1.22048,0 2.21526,-1.0031 2.21526,-2.23471 v 0 -4.30358 c 0,-1.23539 -0.99478,-2.23642 -2.21526,-2.23642 v 0 z m -198.56763,0 c -1.22461,0 -2.21872,1.00103 -2.21872,2.23642 v 0 4.30358 c 0,1.23161 0.99411,2.23471 2.21872,2.23471 v 0 h 4.40016 c 1.22494,0 2.2163,-1.0031 2.2163,-2.23471 v 0 -4.30358 c 0,-1.23539 -0.99136,-2.23642 -2.2163,-2.23642 v 0 z\"\n         id=\"path836\"\n         style=\"stroke-width:0.389833\" />\n      <g\n         id=\"g1400\">\n        <path\n           style=\"fill:url(#linearGradient1468);fill-opacity:1;stroke-width:3.05778\"\n           d=\"M 167.92969,0.00281082 C 153.91385,0.06793434 140.52908,1.2632881 128.75185,3.3472609 94.057586,9.4765819 87.758461,22.305815 87.758461,45.965099 V 77.211816 H 169.74524 V 87.627382 H 87.758461 56.98953 c -23.827649,0 -44.691815,14.321798 -51.2178462,41.566738 -7.5277182,31.229 -7.8616278,50.71643 0,83.32456 5.8278802,24.2722 19.7457432,41.56673 43.5733922,41.56673 h 28.188922 v -37.45783 c 0,-27.06107 23.413862,-50.9312 51.217852,-50.9312 h 81.89123 c 22.79561,0 40.99339,-18.76918 40.99339,-41.66228 V 45.965099 c 0,-22.218887 -18.74415,-38.9096022 -40.99339,-42.6178381 C 196.55897,1.0027638 181.94549,-0.0623127 167.92969,0.00281082 Z M 123.59184,25.133957 c 8.46866,0 15.38447,7.02878 15.38447,15.671135 -3e-5,8.611724 -6.91581,15.575583 -15.38447,15.575583 -8.49904,0 -15.38446,-6.963859 -15.38446,-15.575583 -3e-5,-8.642355 6.88542,-15.671135 15.38446,-15.671135 z\"\n           id=\"path1948\" />\n        <path\n           style=\"fill:url(#linearGradient1465);fill-opacity:1;stroke-width:3.05157\"\n           d=\"m 372.11228,194.486 v 36.33276 c 0,28.16828 -23.88128,51.87669 -51.11379,51.87669 h -81.72487 c -22.38583,0 -40.91011,19.15922 -40.91011,41.57764 v 77.9104 c 0,22.17374 19.28159,35.21609 40.91011,41.57764 25.89969,7.61553 50.73611,8.99185 81.72487,0 20.59855,-5.96395 40.9101,-17.96645 40.9101,-41.57764 v -31.18324 h -81.72486 v -10.3944 h 81.72486 40.91011 c 23.77924,0 32.64036,-16.58653 40.91008,-41.48229 8.54236,-25.6298 8.17888,-50.27698 0,-83.15527 C 437.85213,212.29592 426.62818,194.486 402.8187,194.486 Z m -45.96427,197.30308 c 8.48175,0 15.35321,6.94971 15.35321,15.54394 -3e-5,8.6248 -6.87146,15.63929 -15.35321,15.63929 -8.45151,0 -15.35321,-7.01449 -15.35321,-15.63929 0,-8.59423 6.9017,-15.54394 15.35321,-15.54394 z\"\n           id=\"path1950\" />\n      </g>\n    </g>\n  </g>\n</svg>\n");

/***/ }),

/***/ "./style/slurmel-icon.svg":
/*!********************************!*\
  !*** ./style/slurmel-icon.svg ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg\n   width=\"40\"\n   height=\"40\"\n   version=\"1.1\"\n   id=\"svg842\"\n   sodipodi:docname=\"Slurm_logo.svg\"\n   inkscape:version=\"1.1.2 (b8e25be833, 2022-02-05)\"\n   viewBox=\"0 0 40 40\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs846\">\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient4689\"\n       id=\"linearGradient1478\"\n       gradientUnits=\"userSpaceOnUse\"\n       gradientTransform=\"matrix(1.7201279,0,0,1.7367347,-45.8396,-35.783308)\"\n       x1=\"26.648937\"\n       y1=\"20.603781\"\n       x2=\"135.66525\"\n       y2=\"114.39767\" />\n    <linearGradient\n       id=\"linearGradient4689\">\n      <stop\n         style=\"stop-color:#5a9fd4;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop4691\" />\n      <stop\n         style=\"stop-color:#306998;stop-opacity:1;\"\n         offset=\"1\"\n         id=\"stop4693\" />\n    </linearGradient>\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient4671\"\n       id=\"linearGradient1475\"\n       gradientUnits=\"userSpaceOnUse\"\n       gradientTransform=\"matrix(1.7166332,0,0,1.7332063,65.036885,71.326052)\"\n       x1=\"150.96111\"\n       y1=\"192.35176\"\n       x2=\"112.03144\"\n       y2=\"137.27299\" />\n    <linearGradient\n       id=\"linearGradient4671\">\n      <stop\n         style=\"stop-color:#ffd43b;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop4673\" />\n      <stop\n         style=\"stop-color:#ffe873;stop-opacity:1\"\n         offset=\"1\"\n         id=\"stop4675\" />\n    </linearGradient>\n  </defs>\n  <sodipodi:namedview\n     id=\"namedview844\"\n     pagecolor=\"#ffffff\"\n     bordercolor=\"#666666\"\n     borderopacity=\"1.0\"\n     inkscape:pageshadow=\"2\"\n     inkscape:pageopacity=\"0.0\"\n     inkscape:pagecheckerboard=\"0\"\n     showgrid=\"false\"\n     inkscape:zoom=\"16.716418\"\n     inkscape:cx=\"14.207589\"\n     inkscape:cy=\"9.0031249\"\n     inkscape:window-width=\"1920\"\n     inkscape:window-height=\"1051\"\n     inkscape:window-x=\"-9\"\n     inkscape:window-y=\"-9\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg842\" />\n  <g\n     id=\"g1421\"\n     transform=\"scale(0.08888889)\">\n    <path\n       fill=\"#42afeb\"\n       d=\"m 217.79209,173.05964 c -3.91294,0 -7.08401,3.14839 -7.08401,7.03332 v 0 13.53739 c 0,3.8822 3.17107,7.03436 7.08401,7.03436 v 0 h 14.07039 c 3.91295,0 7.08917,-3.15216 7.08917,-7.03436 v 0 -13.53739 c 0,-3.88493 -3.17622,-7.03332 -7.08917,-7.03332 v 0 z m 34.58434,21.41998 c -2.93919,0 -5.32283,2.4077 -5.32283,5.36973 v 0 10.33007 c 0,2.96509 2.38364,5.3711 5.32283,5.3711 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40601 5.32111,-5.3711 v 0 -10.33007 c 0,-2.96203 -2.38158,-5.36973 -5.32111,-5.36973 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.4077 -5.32216,5.36973 v 0 10.33007 c 0,2.96509 2.38399,5.3711 5.32216,5.3711 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40601 5.32283,-5.3711 v 0 -10.33007 c 0,-2.96203 -2.38502,-5.36973 -5.32283,-5.36973 v 0 z m 31.08578,11.84875 c -3.91294,0 -7.08401,3.14668 -7.08401,7.03403 v 0 13.53634 c 0,3.88425 3.17107,7.03538 7.08401,7.03538 v 0 h 14.07039 c 3.91295,0 7.08917,-3.15113 7.08917,-7.03538 v 0 -13.53634 c 0,-3.88735 -3.17622,-7.03403 -7.08917,-7.03403 v 0 z m 61.77894,6.3461 c -2.18592,0 -3.95779,1.78763 -3.95779,3.99527 v 0 7.6846 c 0,2.20284 1.77187,3.99184 3.95779,3.99184 v 0 h 7.86453 c 2.18456,0 3.9578,-1.789 3.9578,-3.99184 v 0 -7.6846 c 0,-2.20764 -1.77324,-3.99527 -3.9578,-3.99527 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.78763 -3.95919,3.99527 v 0 7.6846 c 0,2.20284 1.77391,3.99184 3.95919,3.99184 v 0 h 7.86208 c 2.18802,0 3.95987,-1.789 3.95987,-3.99184 v 0 -7.6846 c 0,-2.20764 -1.77185,-3.99527 -3.95987,-3.99527 v 0 z m 89.81026,8.08783 c -2.93919,0 -5.32283,2.40394 -5.32283,5.3663 v 0 10.33349 c 0,2.96271 2.38364,5.36766 5.32283,5.36766 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40495 5.32111,-5.36766 v 0 -10.33349 c 0,-2.96236 -2.38158,-5.3663 -5.32111,-5.3663 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.40394 -5.32216,5.3663 v 0 10.33349 c 0,2.96271 2.38399,5.36766 5.32216,5.36766 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40495 5.32283,-5.36766 v 0 -10.33349 c 0,-2.96236 -2.38502,-5.3663 -5.32283,-5.3663 v 0 z m 92.86472,13.01732 c -2.18592,0 -3.95779,1.78659 -3.95779,3.99149 v 0 7.68494 c 0,2.20319 1.77187,3.99252 3.95779,3.99252 v 0 h 7.86453 c 2.18456,0 3.9578,-1.78933 3.9578,-3.99252 v 0 -7.68494 c 0,-2.2049 -1.77324,-3.99149 -3.9578,-3.99149 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.78659 -3.95919,3.99149 v 0 7.68494 c 0,2.20319 1.77391,3.99252 3.95919,3.99252 v 0 h 7.86208 c 2.18802,0 3.95987,-1.78933 3.95987,-3.99252 v 0 -7.68494 c 0,-2.2049 -1.77185,-3.99149 -3.95987,-3.99149 v 0 z m 55.22592,5.528 c -3.91294,0 -7.08401,3.14975 -7.08401,7.03505 v 0 13.53736 c 0,3.88462 3.17107,7.03199 7.08401,7.03199 v 0 h 14.07039 c 3.91295,0 7.08917,-3.14737 7.08917,-7.03199 v 0 -13.53736 c 0,-3.8853 -3.17622,-7.03505 -7.08917,-7.03505 v 0 z m 85.02057,5.78359 c -1.62555,0 -2.94057,1.32854 -2.94057,2.96508 v 0 5.70443 c 0,1.63654 1.31502,2.96272 2.94057,2.96272 v 0 H 308.65 c 1.62072,0 2.93469,-1.32618 2.93469,-2.96272 v 0 -5.70443 c 0,-1.63654 -1.31397,-2.96508 -2.93469,-2.96508 v 0 z m -161.45955,0 c -1.62317,0 -2.93816,1.32854 -2.93816,2.96508 v 0 5.70443 c 0,1.63654 1.31499,2.96272 2.93816,2.96272 v 0 h 5.83491 c 1.62418,0 2.93885,-1.32618 2.93885,-2.96272 v 0 -5.70443 c 0,-1.63654 -1.31467,-2.96508 -2.93885,-2.96508 v 0 z m 111.02332,1.95856 c -2.93919,0 -5.32283,2.40223 -5.32283,5.36527 v 0 10.33144 c 0,2.96509 2.38364,5.36938 5.32283,5.36938 v 0 h 10.57151 c 2.93953,0 5.32111,-2.40429 5.32111,-5.36938 v 0 -10.33144 c 0,-2.96304 -2.38158,-5.36527 -5.32111,-5.36527 v 0 z m -65.67012,0 c -2.93817,0 -5.32216,2.40223 -5.32216,5.36527 v 0 10.33144 c 0,2.96509 2.38399,5.36938 5.32216,5.36938 v 0 h 10.5708 c 2.93781,0 5.32283,-2.40429 5.32283,-5.36938 v 0 -10.33144 c 0,-2.96304 -2.38502,-5.36527 -5.32283,-5.36527 v 0 z m 92.86472,7.99259 c -2.18592,0 -3.95779,1.79139 -3.95779,3.99834 v 0 7.68288 c 0,2.20729 1.77187,3.99184 3.95779,3.99184 v 0 h 7.86453 c 2.18456,0 3.9578,-1.78455 3.9578,-3.99184 v 0 -7.68288 c 0,-2.20695 -1.77324,-3.99834 -3.9578,-3.99834 v 0 z m -117.00486,0 c -2.18528,0 -3.95919,1.79139 -3.95919,3.99834 v 0 7.68288 c 0,2.20729 1.77391,3.99184 3.95919,3.99184 v 0 h 7.86208 c 2.18802,0 3.95987,-1.78455 3.95987,-3.99184 v 0 -7.68288 c 0,-2.20695 -1.77185,-3.99834 -3.95987,-3.99834 v 0 z m 140.24649,7.42285 c -1.62555,0 -2.94057,1.3272 -2.94057,2.96374 v 0 5.70443 c 0,1.63346 1.31502,2.9651 2.94057,2.9651 v 0 H 308.65 c 1.62072,0 2.93469,-1.33164 2.93469,-2.9651 v 0 -5.70443 c 0,-1.63654 -1.31397,-2.96374 -2.93469,-2.96374 v 0 z m -161.45955,0 c -1.62317,0 -2.93816,1.3272 -2.93816,2.96374 v 0 5.70443 c 0,1.63346 1.31499,2.9651 2.93816,2.9651 v 0 h 5.83491 c 1.62418,0 2.93885,-1.33164 2.93885,-2.9651 v 0 -5.70443 c 0,-1.63654 -1.31467,-2.96374 -2.93885,-2.96374 v 0 z m 180.73096,5.69999 c -1.22528,0 -2.22078,1.00103 -2.22078,2.23642 v 0 4.30358 c 0,1.23161 0.9955,2.23471 2.22078,2.23471 v 0 h 4.40293 c 1.22048,0 2.21526,-1.0031 2.21526,-2.23471 v 0 -4.30358 c 0,-1.23539 -0.99478,-2.23642 -2.21526,-2.23642 v 0 z m -198.56763,0 c -1.22461,0 -2.21872,1.00103 -2.21872,2.23642 v 0 4.30358 c 0,1.23161 0.99411,2.23471 2.21872,2.23471 v 0 h 4.40016 c 1.22494,0 2.2163,-1.0031 2.2163,-2.23471 v 0 -4.30358 c 0,-1.23539 -0.99136,-2.23642 -2.2163,-2.23642 v 0 z\"\n       id=\"path836\"\n       style=\"stroke-width:0.389833\" />\n    <g\n       id=\"g1400\">\n      <path\n         style=\"fill:url(#linearGradient1478);fill-opacity:1;stroke-width:3.05778\"\n         d=\"M 167.92969,0.00281082 C 153.91385,0.06793434 140.52908,1.2632881 128.75185,3.3472609 94.057586,9.4765819 87.758461,22.305815 87.758461,45.965099 V 77.211816 H 169.74524 V 87.627382 H 87.758461 56.98953 c -23.827649,0 -44.691815,14.321798 -51.2178462,41.566738 -7.5277182,31.229 -7.8616278,50.71643 0,83.32456 5.8278802,24.2722 19.7457432,41.56673 43.5733922,41.56673 h 28.188922 v -37.45783 c 0,-27.06107 23.413862,-50.9312 51.217852,-50.9312 h 81.89123 c 22.79561,0 40.99339,-18.76918 40.99339,-41.66228 V 45.965099 c 0,-22.218887 -18.74415,-38.9096022 -40.99339,-42.6178381 C 196.55897,1.0027638 181.94549,-0.0623127 167.92969,0.00281082 Z M 123.59184,25.133957 c 8.46866,0 15.38447,7.02878 15.38447,15.671135 -3e-5,8.611724 -6.91581,15.575583 -15.38447,15.575583 -8.49904,0 -15.38446,-6.963859 -15.38446,-15.575583 -3e-5,-8.642355 6.88542,-15.671135 15.38446,-15.671135 z\"\n         id=\"path1948\" />\n      <path\n         style=\"fill:url(#linearGradient1475);fill-opacity:1;stroke-width:3.05157\"\n         d=\"m 372.11228,194.486 v 36.33276 c 0,28.16828 -23.88128,51.87669 -51.11379,51.87669 h -81.72487 c -22.38583,0 -40.91011,19.15922 -40.91011,41.57764 v 77.9104 c 0,22.17374 19.28159,35.21609 40.91011,41.57764 25.89969,7.61553 50.73611,8.99185 81.72487,0 20.59855,-5.96395 40.9101,-17.96645 40.9101,-41.57764 v -31.18324 h -81.72486 v -10.3944 h 81.72486 40.91011 c 23.77924,0 32.64036,-16.58653 40.91008,-41.48229 8.54236,-25.6298 8.17888,-50.27698 0,-83.15527 C 437.85213,212.29592 426.62818,194.486 402.8187,194.486 Z m -45.96427,197.30308 c 8.48175,0 15.35321,6.94971 15.35321,15.54394 -3e-5,8.6248 -6.87146,15.63929 -15.35321,15.63929 -8.45151,0 -15.35321,-7.01449 -15.35321,-15.63929 0,-8.59423 6.9017,-15.54394 15.35321,-15.54394 z\"\n         id=\"path1950\" />\n    </g>\n  </g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.f1967ab3b40f91efe4c7.js.map