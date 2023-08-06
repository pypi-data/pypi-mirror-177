import { InternalAPIRequest } from "../../tools/fetcher.js";
import { flaskES6 } from "../../../app.js";
import { ModalConfirm } from "../../components/modalConfirm.js";
import { FlashMessageTypes, FlashMessage } from "../../components/flash.js";


export class EnergyConsumptionConfigView {

    #internalAPIRequester = null;
    #postReqID = null;
    #putReqID = null;
    #deleteReqID = null;

    #messagesElmt = null;

    #dashboardConfigTableElmt = null;
    #dashboardConfigTableBodyElmt = null;
    #dashboardConfigTableFooterElmt = null;
    // #energySourceConfigElmt = null;
    #addEnergySourceBtnElmt = null;
    #addEnergySourceMenuElmt = null;
    #saveSelectedTimeseriesBtnElmt = null;

    #structuralElement = {};
    #dashboardConfig = null;
    #energySources = {};
    #energyUses = {};
    // #definedEnergySources = [];
    #availableEnergySources = [];
    #tsSelector = null;
    #isEditable = false;

    #selectTimeseriesModalElmt = null;
    #selectTimeseriesModal = null;
    #editedEnergySourceInputElmt = null;
    #editedEnergyUseInputElmt = null;
    #editedEnergySourceNameElmt = null;
    #editedEnergyUseNameElmt = null;
    #editedWhFactorInputElmt = null;

    constructor(structuralElement, dashboardConfig, energySources, energyUses, availableEnergySources, tsSelector, isEditable) {
        this.#structuralElement = structuralElement;
        this.#dashboardConfig = dashboardConfig;
        this.#energySources = energySources;
        this.#energyUses = energyUses;
        this.#availableEnergySources = availableEnergySources;
        this.#tsSelector = tsSelector;
        this.#isEditable = isEditable;

        this.#cacheDOM();
        this.#initEventListeners();

        this.#internalAPIRequester = new InternalAPIRequest();
    }

    #cacheDOM() {
        this.#messagesElmt = document.getElementById("messages");

        this.#dashboardConfigTableElmt = document.getElementById("dashboardConfigTable");
        this.#dashboardConfigTableBodyElmt = this.#dashboardConfigTableElmt.querySelector("tbody");
        this.#dashboardConfigTableFooterElmt = this.#dashboardConfigTableElmt.querySelector("tfoot");
        // this.#energySourceConfigElmt = document.getElementById("energySourceConfig");
        this.#addEnergySourceBtnElmt = document.getElementById("addEnergySourceBtn");
        this.#addEnergySourceMenuElmt = this.#addEnergySourceBtnElmt.parentElement.querySelector("ul.dropdown-menu");
        this.#saveSelectedTimeseriesBtnElmt = document.getElementById("saveSelectedTimeseriesBtn");

        this.#selectTimeseriesModalElmt = document.getElementById("selectTimeseries");
        this.#selectTimeseriesModal = new bootstrap.Modal(this.#selectTimeseriesModalElmt);

        this.#editedEnergySourceInputElmt = this.#selectTimeseriesModalElmt.querySelector("#editedEnergySource");
        this.#editedEnergyUseInputElmt = this.#selectTimeseriesModalElmt.querySelector("#editedEnergyUse");
        this.#editedEnergySourceNameElmt = this.#selectTimeseriesModalElmt.querySelector("#editedEnergySourceName");
        this.#editedEnergyUseNameElmt = this.#selectTimeseriesModalElmt.querySelector("#editedEnergyUseName");

        this.#editedWhFactorInputElmt = document.getElementById("editedWhFactor");
    }

    #initEventListeners() {

        // this.#addEnergySourceBtnElmt.addEventListener("click", (event) => {
        //     console.log("addEnergySourceBtnElmt click");
        // });

        // this.#addEnergySourceBtnElmt.addEventListener("change", (event) => {
        //     console.log("addEnergySourceBtnElmt change");
        // });


        this.#tsSelector.addEventListener("toggleItem", (event) => {
            event.preventDefault();

            this.#updateSaveBtnState();
        });


        this.#saveSelectedTimeseriesBtnElmt.addEventListener("click", (event) => {
            event.preventDefault();

            console.log("save selected timeseries");
            console.log(this.#tsSelector.selectedItemIds);
            console.log(this.#tsSelector.selectedItemNames);

            // save selection in database, post or put

            if (this.#postReqID != null) {
                this.#internalAPIRequester.abort(this.#postReqID);
                this.#postReqID = null;
            }
            if (this.#putReqID != null) {
                this.#internalAPIRequester.abort(this.#putReqID);
                this.#putReqID = null;
            }

            let payload = {
                structural_element_type: this.#structuralElement.type,
                structural_element_id: this.#structuralElement.id,
                energy_source_id: this.#editedEnergySourceInputElmt.value,
                energy_use_id: this.#editedEnergyUseInputElmt.value,
                timeseries_id: this.#tsSelector.selectedItemIds[0],
                wh_factor: this.#editedWhFactorInputElmt.value,
            };


            let energyConsTs = this.#getEnergyConsTs(this.#editedEnergySourceInputElmt.value, this.#editedEnergyUseInputElmt.value);

            // let idSuffix = `${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`;

            // let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
            
            // if (configIdElmt.value == "") {
            if (energyConsTs.id == null) {

                // post
                this.#postReqID = this.#internalAPIRequester.post(
                    flaskES6.urlFor(`api.dashboards.energy_consumption.create`),
                    payload,
                    (data) => {

                        let confData = this.#dashboardConfig[this.#editedEnergySourceInputElmt.value].energy_uses[this.#editedEnergyUseInputElmt.value];

                        confData.id = data.data.id;
                        confData.ts_id = data.data.timeseries_id;
                        confData.ts_name = data.data.ts_name;
                        confData.ts_unit = data.data.ts_unit;
                        confData.wh_factor = data.data.wh_conversion_factor;
                        confData.etag = data.etag;

                        this.#dashboardConfig[this.#editedEnergySourceInputElmt.value].energy_uses[this.#editedEnergyUseInputElmt.value] = confData;


                        this.#refreshConf(this.#editedEnergySourceInputElmt.value, this.#editedEnergyUseInputElmt.value);



                        // // if post update config id hidden input
                        // let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // configIdElmt.value = data.data.id;

                        // let etagElmt = document.getElementById(`etag-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // etagElmt.value = data.etag;

                        // let btnDeleteConfigElmt = document.getElementById(`btnDelConfig-${idSuffix}`);
                        // btnDeleteConfigElmt.classList.remove("d-none");


                        // let tsIdCellElmt = document.getElementById(`tsId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // tsIdCellElmt.value = this.#tsSelector.selectedItemIds[0];


                        // let tsTargetCellElmt = document.getElementById(`tsSpan-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // tsTargetCellElmt.innerText = `[${this.#tsSelector.selectedItemNames[0]}]`;

                        // let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // whFactorTargetCellElmt.innerText = `x${this.#editedWhFactorInputElmt.value}`;
                        // whFactorTargetCellElmt.classList.remove("d-none");

                        // let whFactorElmt = document.getElementById(`whFactor-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // whFactorElmt.value = this.#editedWhFactorInputElmt.value;

                        // let tsConfigCellElmt = document.getElementById(`tsConfigCell-${idSuffix}`);
                        // tsConfigCellElmt.classList.remove("table-warning");

                    },
                    (error) => {
                        let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.ERROR, text: error.toString(), isDismissible: true});
                        this.#messagesElmt.appendChild(flashMsgElmt);
                    },
                    () => {
                        this.#selectTimeseriesModal.hide();

                        let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.SUCCESS, text: `[${this.#editedEnergySourceNameElmt.innerText} - ${this.#editedEnergyUseNameElmt.innerText}] energy consumption configuration saved!`, isDismissible: true});
                        this.#messagesElmt.appendChild(flashMsgElmt);
                    },
                );

            }
            else {

                // update
                // let etagElmt = document.getElementById(`etag-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);

                this.#putReqID = this.#internalAPIRequester.put(
                    flaskES6.urlFor(`api.dashboards.energy_consumption.update`, {id: energyConsTs.id}),
                    payload,
                    energyConsTs.etag,
                    (data) => {

                        let confData = this.#dashboardConfig[this.#editedEnergySourceInputElmt.value].energy_uses[this.#editedEnergyUseInputElmt.value];

                        // confData.id = data.data.id;
                        confData.ts_id = data.data.timeseries_id;
                        confData.ts_name = data.data.ts_name;
                        confData.ts_unit = data.data.ts_unit;
                        confData.wh_factor = data.data.wh_conversion_factor;
                        confData.etag = data.etag;

                        this.#dashboardConfig[this.#editedEnergySourceInputElmt.value].energy_uses[this.#editedEnergyUseInputElmt.value] = confData;


                        this.#refreshConf(this.#editedEnergySourceInputElmt.value, this.#editedEnergyUseInputElmt.value);


                        // let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // configIdElmt.value = data.data.id;

                        // let etagElmt = document.getElementById(`etag-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // etagElmt.value = data.etag;

                        // let btnDeleteConfigElmt = document.getElementById(`btnDelConfig-${idSuffix}`);
                        // btnDeleteConfigElmt.classList.remove("d-none");


                        // let tsIdCellElmt = document.getElementById(`tsId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // tsIdCellElmt.value = this.#tsSelector.selectedItemIds[0];


                        // let tsTargetCellElmt = document.getElementById(`tsSpan-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // tsTargetCellElmt.innerText = `[${this.#tsSelector.selectedItemNames[0]}]`;

                        // let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // whFactorTargetCellElmt.innerText = `x${this.#editedWhFactorInputElmt.value}`;
                        // whFactorTargetCellElmt.classList.remove("d-none");

                        // let whFactorElmt = document.getElementById(`whFactor-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // whFactorElmt.value = this.#editedWhFactorInputElmt.value;

                        // let tsConfigCellElmt = document.getElementById(`tsConfigCell-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                        // tsConfigCellElmt.classList.remove("table-warning");
                    },
                    (error) => {
                        let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.ERROR, text: error.toString(), isDismissible: true});
                        this.#messagesElmt.appendChild(flashMsgElmt);
                    },
                    () => {
                        this.#selectTimeseriesModal.hide();

                        let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.SUCCESS, text: `[${this.#editedEnergySourceNameElmt.innerText} - ${this.#editedEnergyUseNameElmt.innerText}] energy consumption configuration saved!`, isDismissible: true});
                        this.#messagesElmt.appendChild(flashMsgElmt);
                    },
                );
            }


        });


        this.#selectTimeseriesModalElmt.addEventListener("show.bs.modal", (event) => {
            this.#tsSelector.clearAllSelection();


            // event.relatedTarget is the button that triggered the modal
            let energySourceId = event.relatedTarget.getAttribute("data-energy-source");
            let energyUseId = event.relatedTarget.getAttribute("data-energy-use");

            let energyConsTs = this.#getEnergyConsTs(energySourceId, energyUseId);

            // this.#editedEnergySourceInputElmt.value = event.relatedTarget.getAttribute("data-energy-source-id");
            // this.#editedEnergyUseInputElmt.value = event.relatedTarget.getAttribute("data-energy-use-id");

            // this.#editedEnergySourceNameElmt.innerText = event.relatedTarget.getAttribute("data-energy-source-name");
            // this.#editedEnergyUseNameElmt.innerText = event.relatedTarget.getAttribute("data-energy-use-name");

            // this.#editedWhFactorInputElmt.value = event.relatedTarget.getAttribute("data-wh-factor");


            this.#editedEnergySourceNameElmt.innerText = this.#energySources[energySourceId];
            this.#editedEnergyUseNameElmt.innerText = this.#energyUses[energyUseId];

            this.#editedEnergySourceInputElmt.value = energySourceId;
            this.#editedEnergyUseInputElmt.value = energyUseId;

            this.#editedWhFactorInputElmt.value = energyConsTs.wh_factor;


            if (energyConsTs.ts_id != null) {
                this.#tsSelector.select(energyConsTs.ts_id, () => { this.#updateSaveBtnState(); });
            }
            else {
                this.#updateSaveBtnState();
            }

        });

    }


    #updateSaveBtnState() {
        if (this.#tsSelector.selectedItemNames.length > 0) {
            this.#saveSelectedTimeseriesBtnElmt.removeAttribute("disabled");
        }
        else {
            this.#saveSelectedTimeseriesBtnElmt.setAttribute("disabled", true);
        }
    }


    #refreshConf(energySourceId, energyUseId) {
        let idSuffix = `${energySourceId}-${energyUseId}`;

        let confData = this.#getEnergyConsTs(energySourceId, energyUseId);

        let spanTsElmt = document.getElementById(`tsSpan-${idSuffix}`);
        spanTsElmt.innerText = `[${confData.ts_id ? confData.ts_name : "none"}]`;

        let spanWhFactorElmt = document.getElementById(`whFactorSpan-${idSuffix}`);
        spanWhFactorElmt.innerText = `x${confData.wh_factor}`;


        let tsConfigTdElmt = document.getElementById(`tsConfigCell-${idSuffix}`);
        let btnDeleteConfigElmt = document.getElementById(`btnDelConfig-${idSuffix}`);

        if (confData.id == null) {
            tsConfigTdElmt.classList.add("table-warning");
            spanWhFactorElmt.classList.add("d-none");
            btnDeleteConfigElmt.classList.add("d-none");
        }
        else {
            tsConfigTdElmt.classList.remove("table-warning");
            spanWhFactorElmt.classList.remove("d-none");
            btnDeleteConfigElmt.classList.remove("d-none");
        }
    }


    // #prepareEnergySourceConfig(energySource) {
    //     let energySourceConfig = {
    //         energySourceId: energySource.id,
    //         energySourceName: energySource.name,
    //         energyUses: {},
    //     };

    //     let energyUses = {};
    //     for (let energyUse of this.#energyUses) {
    //         energyUses[energyUse.id] = {
    //             energyUseName: energyUse.name,
    //             id: null,
    //             tsId: null,
    //             whFactor: 1,
    //         };
    //     }

    //     energySourceConfig.energyUses = energyUses;

    //     return energySourceConfig;
    // }


    // #addEnergySourceConfig(energySourceConfig) {

    //     console.log(energySourceConfig);

    //     let rowElmt = document.createElement("tr");
    //     rowElmt.classList.add("align-middle");

    //     let thElmt = document.createElement("th");
    //     thElmt.classList.add("text-center", "text-break");
    //     thElmt.setAttribute("scope", "row");
    //     thElmt.innerText = energySourceConfig.energySourceName;
    //     rowElmt.appendChild(thElmt);

    //     for (let [energyUseId, tsConfig] of Object.entries(energySourceConfig.energyUses)) {

    //         let tsConfigTdElmt = document.createElement("td");
    //         // tsConfigTdElmt.classList.add("text-center");
    //         tsConfigTdElmt.id = `tsConfigCell-${energySourceConfig.energySourceId}-${energyUseId}`;

    //         let tdContainerElmt = document.createElement("div");
    //         tdContainerElmt.classList.add("d-flex", "justify-content-between", "align-items-center", "gap-2", "p-2");

    //         let tdSpanContainerElmt = document.createElement("div");
    //         tdSpanContainerElmt.classList.add("d-flex", "flex-wrap", "align-items-center", "gap-2");

    //         let spanTsElmt = document.createElement("span");
    //         spanTsElmt.classList.add("text-break");
    //         spanTsElmt.id = `tsSpan-${energySourceConfig.energySourceId}-${energyUseId}`;
    //         spanTsElmt.innerText = `[${tsConfig.tsId ? tsConfig.tsId : "none"}]`;

    //         let spanWhFactorElmt = document.createElement("span");
    //         spanWhFactorElmt.id = `whFactorSpan-${energySourceConfig.energySourceId}-${energyUseId}`;
    //         spanWhFactorElmt.innerText = `x${tsConfig.whFactor}`;

    //         // if (tsConfig.id != null) {
    //         //     spanTsElmt.innerText = tsConfig.tsId;
    //         //     spanWhFactorElmt.innerText = `x${tsConfig.whFactor}`;
    //         // }
    //         if (tsConfig.id == null) {
    //             tsConfigTdElmt.classList.add("table-warning");
    //             spanWhFactorElmt.classList.add("d-none");
    //         }

    //         tdSpanContainerElmt.appendChild(spanTsElmt);
    //         tdSpanContainerElmt.appendChild(spanWhFactorElmt);

    //         tdContainerElmt.appendChild(tdSpanContainerElmt);


    //         if (this.#isEditable) {

    //             let configIdInputElmt = document.createElement("input");
    //             configIdInputElmt.setAttribute("type", "hidden");
    //             configIdInputElmt.id = `configId-${energySourceConfig.energySourceId}-${energyUseId}`;
    //             configIdInputElmt.value = tsConfig.id;
    //             tdContainerElmt.appendChild(configIdInputElmt);

    //             let etagInputElmt = document.createElement("input");
    //             etagInputElmt.setAttribute("type", "hidden");
    //             etagInputElmt.id = `etag-${energySourceConfig.energySourceId}-${energyUseId}`;
    //             tdContainerElmt.appendChild(etagInputElmt);

    //             let tsIdInputElmt = document.createElement("input");
    //             tsIdInputElmt.setAttribute("type", "hidden");
    //             tsIdInputElmt.id = `tsId-${energySourceConfig.energySourceId}-${energyUseId}`;
    //             tsIdInputElmt.value = tsConfig.tsId;
    //             tdContainerElmt.appendChild(tsIdInputElmt);

    //             let whFactorInputElmt = document.createElement("input");
    //             whFactorInputElmt.setAttribute("type", "hidden");
    //             whFactorInputElmt.id = `whFactor-${energySourceConfig.energySourceId}-${energyUseId}`;
    //             whFactorInputElmt.value = tsConfig.whFactor;
    //             tdContainerElmt.appendChild(whFactorInputElmt);


    //             let editContainerElmt = document.createElement("div");
    //             editContainerElmt.classList.add("d-grid", "gap-1");


    //             let btnModalTimeseriesSelectorElmt = document.createElement("button");
    //             btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-sm", "btn-outline-secondary");
    //             btnModalTimeseriesSelectorElmt.setAttribute("data-bs-toggle", "modal");
    //             btnModalTimeseriesSelectorElmt.setAttribute("data-bs-target", "#selectTimeseries");
    //             // btnModalTimeseriesSelectorElmt.setAttribute("data-wh-factor", tsConfig.whFactor);
    //             // btnModalTimeseriesSelectorElmt.id = `tsModalBtn-${energySourceConfig.energySourceId}-${energyUseId}`;

    //             let editIconElmt = document.createElement("i");
    //             editIconElmt.classList.add("bi", "bi-pencil");

    //             btnModalTimeseriesSelectorElmt.appendChild(editIconElmt);

    //             btnModalTimeseriesSelectorElmt.addEventListener("click", (event) => {
    //                 this.#editedEnergySourceNameElmt.innerText = energySourceConfig.energySourceName;
    //                 this.#editedEnergyUseNameElmt.innerText = tsConfig.energyUseName;

    //                 this.#editedEnergySourceInputElmt.value = energySourceConfig.energySourceId;
    //                 this.#editedEnergyUseInputElmt.value = energyUseId;

    //                 // this.#editedWhFactorInputElmt.value = tsConfig.whFactor;
    //                 this.#editedWhFactorInputElmt.value = whFactorInputElmt.value;

    //                 if (tsIdInputElmt.value.length > 0) {
    //                     this.#tsSelector.select(tsIdInputElmt.value, () => { this.#updateSaveBtnState(); });
    //                 }
    //             });

    //             editContainerElmt.appendChild(btnModalTimeseriesSelectorElmt);


    //             let btnDeleteElmt = document.createElement("button");
    //             btnDeleteElmt.classList.add("btn", "btn-sm", "btn-outline-danger");
    //             btnDeleteElmt.id = `btnDelConfig-${energySourceConfig.energySourceId}-${energyUseId}`;

    //             let delIconElmt = document.createElement("i");
    //             delIconElmt.classList.add("bi", "bi-trash");
    //             btnDeleteElmt.appendChild(delIconElmt);

    //             if (tsConfig.id == null) {
    //                 btnDeleteElmt.classList.add("d-none");
    //             }

    //             // Add a modal confirm component for this item, defining an "ok" callback function to remove it.
    //             let modalConfirm = new ModalConfirm(configIdInputElmt.id, `Remove <mark>${energySourceConfig.energySourceName} - ${tsConfig.energyUseName}</mark> energy consumption configuration`, () => {

    //                 console.log("!!! remove callback !!!");


    //                 console.log("delete ts config");

    //                 let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
    //                 let etagElmt = document.getElementById(`etag-${energySourceConfig.energySourceId}-${energyUseId}`);

    //                 // delete using config id -> configIdElmt.value

    //                 if (this.#deleteReqID != null) {
    //                     this.#internalAPIRequester.abort(this.#deleteReqID);
    //                     this.#deleteReqID = null;
    //                 }

    //                 this.#deleteReqID = this.#internalAPIRequester.delete(
    //                     flaskES6.urlFor(`api.dashboards.energy_consumption.delete`, {id: configIdElmt.value, structural_element_type: this.#structuralElement.type}),
    //                     etagElmt.value,
    //                     () => {
    //                         configIdElmt.value = "";

    //                         let tsTargetCellElmt = document.getElementById(`tsSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
    //                         tsTargetCellElmt.innerText = `[none]`;

    //                         let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
    //                         whFactorTargetCellElmt.innerText = `x1`;
    //                         whFactorTargetCellElmt.classList.add("d-none");

    //                         let whFactorElmt = document.getElementById(`whFactor-${energySourceConfig.energySourceId}-${energyUseId}`);
    //                         whFactorElmt.value = 1;

    //                         let tsConfigCellElmt = document.getElementById(`tsConfigCell-${energySourceConfig.energySourceId}-${energyUseId}`);
    //                         tsConfigCellElmt.classList.add("table-warning");

    //                         btnDeleteElmt.classList.add("d-none");


    //                         this.#editedEnergySourceInputElmt.value = "";
    //                         this.#editedEnergyUseInputElmt.value = "";
    //                         this.#editedEnergySourceNameElmt.value = "";
    //                         this.#editedEnergyUseNameElmt.value = "";
    //                         this.#editedWhFactorInputElmt.value = "";

    //                         configIdInputElmt.value = "";
    //                         etagInputElmt.value = "";
    //                         tsIdInputElmt.value = "";
    //                         whFactorInputElmt.value = "1";
    //                     },
    //                     (error) => {
    //                         let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.ERROR, text: error.toString(), isDismissible: true});
    //                         this.#messagesElmt.appendChild(flashMsgElmt);
    //                     },
    //                     () => {
    //                         let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.SUCCESS, text: `[${energySourceConfig.energySourceName} - ${tsConfig.energyUseName}] energy consumption configuration removed!`, isDismissible: true});
    //                         this.#messagesElmt.appendChild(flashMsgElmt);
    //                     },
    //                 );


    //             });
    //             editContainerElmt.appendChild(modalConfirm);

    //             // Add an event listener to display a confirm message on delete button click.
    //             btnDeleteElmt.addEventListener("click", (event) => {
    //                 event.preventDefault();
    //                 // Display modal.
    //                 modalConfirm.show();
    //             });

    //             // btnDeleteElmt.addEventListener("click", (event) => {
    //             //     console.log("delete ts config");

    //             //     let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);

    //             //     // delete using config id -> configIdElmt.value

    //             //     configIdElmt.value = "";


    //             //     let tsTargetCellElmt = document.getElementById(`tsSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
    //             //     tsTargetCellElmt.innerText = `[none]`;

    //             //     let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
    //             //     whFactorTargetCellElmt.innerText = `x1`;
    //             //     whFactorTargetCellElmt.classList.add("d-none");

    //             //     let whFactorElmt = document.getElementById(`whFactor-${energySourceConfig.energySourceId}-${energyUseId}`);
    //             //     whFactorElmt.value = 1;

    //             //     let tsConfigCellElmt = document.getElementById(`tsConfigCell-${energySourceConfig.energySourceId}-${energyUseId}`);
    //             //     tsConfigCellElmt.classList.add("table-warning");

    //             //     btnDeleteElmt.classList.add("d-none");
    //             // });


    //             editContainerElmt.appendChild(btnDeleteElmt);

    //             tdContainerElmt.appendChild(editContainerElmt);

    //         }

    //         tsConfigTdElmt.appendChild(tdContainerElmt);

    //         rowElmt.appendChild(tsConfigTdElmt);
    //     }

    //     this.#dashboardConfigTableBodyElmt.appendChild(rowElmt);

    // }


    #getEnergyConsTs(energySourceId, energyUseId) {

        return this.#dashboardConfig[energySourceId].energy_uses[energyUseId];
    }


    #addEnergySourceFromConfig(energySourceConfigData) {

        console.log(energySourceConfigData);

        let rowElmt = document.createElement("tr");
        rowElmt.classList.add("align-middle");

        let thElmt = document.createElement("th");
        thElmt.classList.add("text-center", "text-break");
        thElmt.setAttribute("scope", "row");
        thElmt.innerText = energySourceConfigData.energy_source_name;
        rowElmt.appendChild(thElmt);

        for (let energyUseId of Object.keys(this.#energyUses)) {

            let configData = energySourceConfigData.energy_uses[energyUseId];


        // for (let [energyUseId, configData] of Object.entries(energySourceConfigData.energy_uses)) {

            let idSuffix = `${energySourceConfigData.energy_source_id}-${energyUseId}`;

            let tsConfigTdElmt = document.createElement("td");
            tsConfigTdElmt.id = `tsConfigCell-${idSuffix}`;

            let tdContainerElmt = document.createElement("div");
            tdContainerElmt.classList.add("d-flex", "justify-content-between", "align-items-center", "gap-2", "p-2");

            let tdSpanContainerElmt = document.createElement("div");
            tdSpanContainerElmt.classList.add("d-flex", "flex-wrap", "align-items-center", "gap-2");

            let spanTsElmt = document.createElement("span");
            spanTsElmt.classList.add("text-break");
            spanTsElmt.id = `tsSpan-${idSuffix}`;
            spanTsElmt.innerText = `[${configData.ts_id ? configData.ts_name : "none"}]`;

            let spanWhFactorElmt = document.createElement("span");
            spanWhFactorElmt.id = `whFactorSpan-${idSuffix}`;
            spanWhFactorElmt.innerText = `x${configData.wh_factor}`;

            if (configData.id == null) {
                tsConfigTdElmt.classList.add("table-warning");
                spanWhFactorElmt.classList.add("d-none");
            }

            tdSpanContainerElmt.appendChild(spanTsElmt);
            tdSpanContainerElmt.appendChild(spanWhFactorElmt);

            tdContainerElmt.appendChild(tdSpanContainerElmt);


            if (this.#isEditable) {

                // let configIdInputElmt = document.createElement("input");
                // configIdInputElmt.setAttribute("type", "hidden");
                // configIdInputElmt.id = `configId-${energySourceConfig.energySourceId}-${energyUseId}`;
                // configIdInputElmt.value = tsConfig.id;
                // tdContainerElmt.appendChild(configIdInputElmt);

                // let etagInputElmt = document.createElement("input");
                // etagInputElmt.setAttribute("type", "hidden");
                // etagInputElmt.id = `etag-${energySourceConfig.energySourceId}-${energyUseId}`;
                // tdContainerElmt.appendChild(etagInputElmt);

                // let tsIdInputElmt = document.createElement("input");
                // tsIdInputElmt.setAttribute("type", "hidden");
                // tsIdInputElmt.id = `tsId-${energySourceConfig.energySourceId}-${energyUseId}`;
                // tsIdInputElmt.value = tsConfig.tsId;
                // tdContainerElmt.appendChild(tsIdInputElmt);

                // let whFactorInputElmt = document.createElement("input");
                // whFactorInputElmt.setAttribute("type", "hidden");
                // whFactorInputElmt.id = `whFactor-${energySourceConfig.energySourceId}-${energyUseId}`;
                // whFactorInputElmt.value = tsConfig.whFactor;
                // tdContainerElmt.appendChild(whFactorInputElmt);


                let editContainerElmt = document.createElement("div");
                editContainerElmt.classList.add("d-grid", "gap-1");


                let btnModalTimeseriesSelectorElmt = document.createElement("button");
                btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-sm", "btn-outline-secondary");
                btnModalTimeseriesSelectorElmt.setAttribute("data-bs-toggle", "modal");
                btnModalTimeseriesSelectorElmt.setAttribute("data-bs-target", "#selectTimeseries");
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source", energySourceConfigData.energy_source_id);
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use", configData.energy_use_id);
                // btnModalTimeseriesSelectorElmt.setAttribute("data-wh-factor", tsConfig.whFactor);
                // btnModalTimeseriesSelectorElmt.id = `tsModalBtn-${energySourceConfig.energySourceId}-${energyUseId}`;

                let editIconElmt = document.createElement("i");
                editIconElmt.classList.add("bi", "bi-pencil");

                btnModalTimeseriesSelectorElmt.appendChild(editIconElmt);

                // btnModalTimeseriesSelectorElmt.addEventListener("click", (event) => {
                //     this.#editedEnergySourceNameElmt.innerText = energySourceConfig.energySourceName;
                //     this.#editedEnergyUseNameElmt.innerText = tsConfig.energyUseName;

                //     this.#editedEnergySourceInputElmt.value = energySourceConfig.energySourceId;
                //     this.#editedEnergyUseInputElmt.value = energyUseId;

                //     // this.#editedWhFactorInputElmt.value = tsConfig.whFactor;
                //     this.#editedWhFactorInputElmt.value = whFactorInputElmt.value;

                //     if (tsIdInputElmt.value.length > 0) {
                //         this.#tsSelector.select(tsIdInputElmt.value, () => { this.#updateSaveBtnState(); });
                //     }
                // });

                editContainerElmt.appendChild(btnModalTimeseriesSelectorElmt);


                let btnDeleteElmt = document.createElement("button");
                btnDeleteElmt.classList.add("btn", "btn-sm", "btn-outline-danger");
                btnDeleteElmt.id = `btnDelConfig-${idSuffix}`;

                let delIconElmt = document.createElement("i");
                delIconElmt.classList.add("bi", "bi-trash");
                btnDeleteElmt.appendChild(delIconElmt);

                if (configData.id == null) {
                    btnDeleteElmt.classList.add("d-none");
                }

                // Add a modal confirm component for this item, defining an "ok" callback function to remove it.
                let modalConfirm = new ModalConfirm(tsConfigTdElmt.id, `Remove <mark>${energySourceConfigData.energy_source_name} - ${configData.energy_use_name}</mark> energy consumption configuration`, () => {

                    console.log("!!! remove callback !!!");


                    console.log("delete ts config");


                    let energyConsTs = this.#getEnergyConsTs(energySourceConfigData.energy_source_id, configData.energy_use_id);


                    // delete using config id -> configIdElmt.value
                    // let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
                    // let etagElmt = document.getElementById(`etag-${energySourceConfig.energySourceId}-${energyUseId}`);


                    if (this.#deleteReqID != null) {
                        this.#internalAPIRequester.abort(this.#deleteReqID);
                        this.#deleteReqID = null;
                    }

                    this.#deleteReqID = this.#internalAPIRequester.delete(
                        flaskES6.urlFor(`api.dashboards.energy_consumption.delete`, {id: energyConsTs.id, structural_element_type: this.#structuralElement.type}),
                        energyConsTs.etag,
                        () => {
                            // configIdElmt.value = "";


                            let confData = this.#dashboardConfig[energySourceConfigData.energy_source_id].energy_uses[configData.energy_use_id];

                            confData.id = null;
                            confData.ts_id = null;
                            confData.ts_name = null;
                            confData.ts_unit = null;
                            confData.wh_factor = 1;
                            confData.etag = null;

                            this.#dashboardConfig[energySourceConfigData.energy_source_id].energy_uses[configData.energy_use_id] = confData;


                            this.#refreshConf(energySourceConfigData.energy_source_id, configData.energy_use_id);


                            // spanTsElmt.innerText = `[${confData.ts_id ? confData.ts_name : "none"}]`;

                            // spanWhFactorElmt.innerText = `x${confData.wh_factor}`;

                            // if (confData.id == null) {
                            //     tsConfigTdElmt.classList.add("table-warning");
                            //     spanWhFactorElmt.classList.add("d-none");
                            // }


                            // let tsTargetCellElmt = document.getElementById(`tsSpan-${idSuffix}`);
                            // tsTargetCellElmt.innerText = `[none]`;

                            // let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
                            // whFactorTargetCellElmt.innerText = `x1`;
                            // whFactorTargetCellElmt.classList.add("d-none");

                            // let whFactorElmt = document.getElementById(`whFactor-${energySourceConfig.energySourceId}-${energyUseId}`);
                            // whFactorElmt.value = 1;

                            // let tsConfigCellElmt = document.getElementById(`tsConfigCell-${energySourceConfig.energySourceId}-${energyUseId}`);
                            // tsConfigCellElmt.classList.add("table-warning");

                            btnDeleteElmt.classList.add("d-none");


                            // this.#editedEnergySourceInputElmt.value = "";
                            // this.#editedEnergyUseInputElmt.value = "";
                            // this.#editedEnergySourceNameElmt.value = "";
                            // this.#editedEnergyUseNameElmt.value = "";
                            // this.#editedWhFactorInputElmt.value = "";

                            // configIdInputElmt.value = "";
                            // etagInputElmt.value = "";
                            // tsIdInputElmt.value = "";
                            // whFactorInputElmt.value = "1";
                        },
                        (error) => {
                            let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.ERROR, text: error.toString(), isDismissible: true});
                            this.#messagesElmt.appendChild(flashMsgElmt);
                        },
                        () => {
                            let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.SUCCESS, text: `[${energySourceConfigData.energy_source_name} - ${configData.energy_use_name}] energy consumption configuration removed!`, isDismissible: true});
                            this.#messagesElmt.appendChild(flashMsgElmt);
                        },
                    );


                });
                editContainerElmt.appendChild(modalConfirm);

                // Add an event listener to display a confirm message on delete button click.
                btnDeleteElmt.addEventListener("click", (event) => {
                    event.preventDefault();
                    // Display modal.
                    modalConfirm.show();
                });

                // btnDeleteElmt.addEventListener("click", (event) => {
                //     console.log("delete ts config");

                //     let configIdElmt = document.getElementById(`configId-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);

                //     // delete using config id -> configIdElmt.value

                //     configIdElmt.value = "";


                //     let tsTargetCellElmt = document.getElementById(`tsSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
                //     tsTargetCellElmt.innerText = `[none]`;

                //     let whFactorTargetCellElmt = document.getElementById(`whFactorSpan-${energySourceConfig.energySourceId}-${energyUseId}`);
                //     whFactorTargetCellElmt.innerText = `x1`;
                //     whFactorTargetCellElmt.classList.add("d-none");

                //     let whFactorElmt = document.getElementById(`whFactor-${energySourceConfig.energySourceId}-${energyUseId}`);
                //     whFactorElmt.value = 1;

                //     let tsConfigCellElmt = document.getElementById(`tsConfigCell-${energySourceConfig.energySourceId}-${energyUseId}`);
                //     tsConfigCellElmt.classList.add("table-warning");

                //     btnDeleteElmt.classList.add("d-none");
                // });


                editContainerElmt.appendChild(btnDeleteElmt);

                tdContainerElmt.appendChild(editContainerElmt);

            }

            tsConfigTdElmt.appendChild(tdContainerElmt);

            rowElmt.appendChild(tsConfigTdElmt);
        }

        this.#dashboardConfigTableBodyElmt.appendChild(rowElmt);

    }

    refresh() {


        this.#dashboardConfigTableBodyElmt.innerHTML = "";


        for (let energySourceConfigData of Object.values(this.#dashboardConfig)) {
            this.#addEnergySourceFromConfig(energySourceConfigData);
        }



        // for (let definedEnergySource of this.#definedEnergySources) {

        //     let energySourceConfig = this.#prepareEnergySourceConfig(definedEnergySource);

        //     for (let tsConfig of this.#dashboardConfig) {
        //         if (tsConfig.source_id == definedEnergySource.id) {
        //             energySourceConfig.energyUses[tsConfig.end_use_id].id = tsConfig.id;
        //             energySourceConfig.energyUses[tsConfig.end_use_id].tsId = tsConfig.timeseries_id;
        //             energySourceConfig.energyUses[tsConfig.end_use_id].whFactor = tsConfig.wh_conversion_factor;
        //         }
        //     }

        //     this.#addEnergySourceConfig(energySourceConfig);

        // }



        if (this.#isEditable) {
            for (let energySourceId of this.#availableEnergySources) {
                let menuItemLinkElmt = document.createElement("a");
                menuItemLinkElmt.classList.add("dropdown-item");
                menuItemLinkElmt.setAttribute("role", "button");
                menuItemLinkElmt.innerText = this.#energySources[energySourceId];

                let menuItemElmt = document.createElement("li");
                menuItemElmt.appendChild(menuItemLinkElmt);

                this.#addEnergySourceMenuElmt.appendChild(menuItemElmt);

                menuItemLinkElmt.addEventListener("click", (event) => {
                    console.log("click on ");
                    console.log(menuItemLinkElmt);
                    console.log(menuItemElmt);

                    menuItemElmt.remove();
                    this.#availableEnergySources = this.#availableEnergySources.filter((availableEnergySource) => availableEnergySource.id != energySourceId);


                    let energyUsesConfigData = {};
                    for (let [energyUseId, energyUseName] in Object.entries(this.#energyUses)) {
                        energyUsesConfigData[energyUseId] = {
                            energy_use_id: energyUseId,
                            energy_use_name: energyUseName,
                            id: null,
                            ts_id: null,
                            ts_name: null,
                            ts_unit: null,
                            wh_factor: 1,
                            etag: null,
                        };
                    }

                    this.#dashboardConfig[energySourceId] = {
                        energy_source_id: energySourceId,
                        energy_source_name: this.#energySources[energySourceId],
                        energy_uses: energyUsesConfigData,
                    };

                    this.#addEnergySourceFromConfig(this.#dashboardConfig[energySourceId]);

                    // let energySourceConfig = this.#prepareEnergySourceConfig(energySource);

                    // this.#addEnergySourceConfig(energySourceConfig);


                    if (this.#availableEnergySources.length <= 0) {
                        this.#dashboardConfigTableFooterElmt.classList.add("d-none");
                    }
                });
            };

            if (this.#availableEnergySources.length <= 0) {
                this.#dashboardConfigTableFooterElmt.classList.add("d-none");
            }
        }
        else {
            this.#dashboardConfigTableFooterElmt?.classList.add("d-none");
        }

    }
}
