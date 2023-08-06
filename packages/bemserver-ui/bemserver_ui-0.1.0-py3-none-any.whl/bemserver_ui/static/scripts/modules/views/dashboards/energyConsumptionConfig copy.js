import { InternalAPIRequest } from "../../tools/fetcher.js";
import { flaskES6, signedUser } from "../../../app.js";
import { Spinner } from "../../components/spinner.js";


export class EnergyConsumptionConfigView {

    #internalAPIRequester = null;
    // #generalReqID = null;
    // #propertiesReqID = null;
    // #tsReqID = null;

    #dashboardConfigTableElmt = null;
    #dashboardConfigTableBodyElmt = null;
    #dashboardConfigTableFooterElmt = null;
    // #energySourceConfigElmt = null;
    #addEnergySourceBtnElmt = null;
    #addEnergySourceMenuElmt = null;
    #saveSelectedTimeseriesBtnElmt = null;

    #dashboardConfig = null;
    #definedEnergySources = [];
    #availableEnergySources = [];
    #energyUses = [];
    #tsSelector = null;
    #isEditable = false;

    #selectTimeseriesModalElmt = null;
    #selectTimeseriesModal = null;
    #editedEnergySourceInputElmt = null;
    #editedEnergyUseInputElmt = null;
    #editedEnergySourceNameElmt = null;
    #editedEnergyUseNameElmt = null;
    #editedWhFactorInputElmt = null;

    constructor(dashBoardConfig, definedEnergySources, availableEnergySources, energyUses, tsSelector, isEditable) {
        this.#dashboardConfig = dashBoardConfig;
        this.#definedEnergySources = definedEnergySources;
        this.#availableEnergySources = availableEnergySources;
        this.#energyUses = energyUses;
        this.#tsSelector = tsSelector;
        this.#isEditable = isEditable;

        this.#cacheDOM();
        this.#initElements();
        this.#initEventListeners();

        this.#internalAPIRequester = new InternalAPIRequest();
    }

    #cacheDOM() {
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

    #initElements() {

        // init tbody

        for (let definedEnergySource of this.#definedEnergySources) {

            // let energySourceConfig = {
            //     sourceId: definedEnergySource.source_id,
            //     sourceName: definedEnergySource.source_name,
            //     energyUses: {},
            // };

            // let energyUses = {};
            // for (let energyUse of this.#energyUses) {
            //     energyUses[energyUse.id] = {
            //         energyUseName: energyUse.name,
            //         id: null,
            //         tsId: null,
            //         whFactor: 1,
            //     };
            // }

            // energySourceConfig.energyUses = energyUses;

            let energySourceConfig = this.#prepareEnergySourceConfig(definedEnergySource);

            for (let tsConfig of this.#dashboardConfig) {
                if (tsConfig.source_id == definedEnergySource.id) {
                    energySourceConfig.energyUses[tsConfig.use_id].id = tsConfig.id;
                    energySourceConfig.energyUses[tsConfig.use_id].tsId = tsConfig.timeseries_id;
                    energySourceConfig.energyUses[tsConfig.use_id].whFactor = tsConfig.wh_conversion_factor;
                }
            }


            this.#addEnergySourceConfig(energySourceConfig);

        }



        if (this.#isEditable) {
            for (let energySource of this.#availableEnergySources) {
                let menuItemLinkElmt = document.createElement("a");
                menuItemLinkElmt.classList.add("dropdown-item");
                menuItemLinkElmt.setAttribute("role", "button");
                // menuItemLinkElmt.setAttribute("data-energy-source-id", energySource.id);
                menuItemLinkElmt.innerText = energySource.name;

                let menuItemElmt = document.createElement("li");
                menuItemElmt.appendChild(menuItemLinkElmt);

                this.#addEnergySourceMenuElmt.appendChild(menuItemElmt);

                menuItemLinkElmt.addEventListener("click", (event) => {
                    console.log("click on ");
                    console.log(menuItemLinkElmt);
                    console.log(menuItemElmt);

                    menuItemElmt.remove();
                    this.#availableEnergySources = this.#availableEnergySources.filter((availableEnergySource) => availableEnergySource.id != energySource.id);


                    // let energySourceConfig = {
                    //     sourceId: energySource.id,
                    //     sourceName: energySource.name,
                    //     energyUses: {},
                    // };

                    // let energyUses = {};
                    // for (let energyUse of this.#energyUses) {
                    //     energyUses[energyUse.id] = {
                    //         energyUseName: energyUse.name,
                    //         id: null,
                    //         tsId: null,
                    //         whFactor: 1,
                    //     };
                    // }

                    // energySourceConfig.energyUses = energyUses;

                    let energySourceConfig = this.#prepareEnergySourceConfig(energySource);

                    this.#addEnergySourceConfig(energySourceConfig);


                    // this.#addEnergySource(energySource);

                    // this.#addTsConfig({ id: null, source_id: energySource.id, source_name: energySource.name, use_id: null });

                    if (this.#availableEnergySources.length <= 0) {
                        // this.#addEnergySourceBtnElmt.classList.add("d-none");
                        this.#dashboardConfigTableFooterElmt.classList.add("d-none");
                    }
                });
            };

            if (this.#availableEnergySources.length <= 0) {
                // this.#addEnergySourceBtnElmt.classList.add("d-none");
                this.#dashboardConfigTableFooterElmt.classList.add("d-none");
            }
        }
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

            if (this.#tsSelector.selectedItemNames.length > 0) {
                this.#saveSelectedTimeseriesBtnElmt.removeAttribute("disabled");
            }
            else {
                this.#saveSelectedTimeseriesBtnElmt.setAttribute("disabled", true);
            }
        });


        this.#saveSelectedTimeseriesBtnElmt.addEventListener("click", (event) => {
            event.preventDefault();

            console.log("save selected timeseries");
            console.log(this.#tsSelector.selectedItemIds);
            console.log(this.#tsSelector.selectedItemNames);

            // save selection in database, post or put


            let targetCellElmt = document.getElementById(`selectedTs-${this.#editedEnergySourceInputElmt.value}-${this.#editedEnergyUseInputElmt.value}`);
            targetCellElmt.innerText = this.#tsSelector.selectedItemNames[0];

            this.#selectTimeseriesModal.hide();
        });


        this.#selectTimeseriesModalElmt.addEventListener("show.bs.modal", (event) => {
            this.#tsSelector.unselectAllResults();

            // event.relatedTarget is the button that triggered the modal
            this.#editedEnergySourceInputElmt.value = event.relatedTarget.getAttribute("data-energy-source-id");
            this.#editedEnergyUseInputElmt.value = event.relatedTarget.getAttribute("data-energy-use-id");

            this.#editedEnergySourceNameElmt.innerText = event.relatedTarget.getAttribute("data-energy-source-name");
            this.#editedEnergyUseNameElmt.innerText = event.relatedTarget.getAttribute("data-energy-use-name");

            this.#editedWhFactorInputElmt.value = event.relatedTarget.getAttribute("data-wh-factor");

        });

    }


    #prepareEnergySourceConfig(energySource) {
        let energySourceConfig = {
            energySourceId: energySource.id,
            energySourceName: energySource.name,
            energyUses: {},
        };

        let energyUses = {};
        for (let energyUse of this.#energyUses) {
            energyUses[energyUse.id] = {
                energyUseName: energyUse.name,
                id: null,
                tsId: null,
                whFactor: 1,
            };
        }

        energySourceConfig.energyUses = energyUses;

        return energySourceConfig;
    }


    #addEnergySourceConfig(energySourceConfig) {

        let row1Elmt = document.createElement("tr");
        row1Elmt.classList.add("align-middle");

        let row2Elmt = document.createElement("tr");
        row2Elmt.classList.add("align-middle");

        let thElmt = document.createElement("th");
        thElmt.classList.add("text-center", "text-break");
        thElmt.setAttribute("scope", "row");
        thElmt.setAttribute("rowspan", "2");
        thElmt.innerText = energySourceConfig.energySourceName;
        row1Elmt.appendChild(thElmt);

        for (let [energyUseId, tsConfig] of Object.entries(energySourceConfig.energyUses)) {

            if (this.#isEditable) {

                let tdTimeseriesElmt = document.createElement("td");
                tdTimeseriesElmt.classList.add("text-center");

                let btnModalTimeseriesSelectorElmt = document.createElement("button");
                btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-sm", "btn-outline-secondary");
                // btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-outline-secondary");
                btnModalTimeseriesSelectorElmt.setAttribute("data-bs-toggle", "modal");
                btnModalTimeseriesSelectorElmt.setAttribute("data-bs-target", "#selectTimeseries");
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-id", energySourceConfig.energySourceId);
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-id", energyUseId);
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-name", energySourceConfig.energySourceName);
                btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-name", tsConfig.energyUseName);
                btnModalTimeseriesSelectorElmt.setAttribute("data-wh-factor", tsConfig.whFactor);
                btnModalTimeseriesSelectorElmt.id = `tsModalBtn-${energySourceConfig.sourceId}-${energyUseId}`;
                btnModalTimeseriesSelectorElmt.innerText = "edit";

                // let selectedTimeseriesElmt = document.createElement("div");
                // // selectedTimeseriesElmt.classList.add("border", "rounded-start", "px-2");
                // selectedTimeseriesElmt.classList.add("input-group-text", "bg-white");
                // selectedTimeseriesElmt.setAttribute("aria-label", "Selected timeseries");
                // selectedTimeseriesElmt.setAttribute("aria-describedby", btnModalTimeseriesSelectorElmt.id);
                // selectedTimeseriesElmt.id = `selectedTs-${energySourceConfig.energySourceId}-${energyUseId}`;
                // selectedTimeseriesElmt.innerText = tsConfig.tsId;

                // inputGroupTimeseriesElmt.appendChild(selectedTimeseriesElmt);

                // inputGroupTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);

                tdTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);
                // tdTimeseriesElmt.appendChild(inputGroupTimeseriesElmt);

                row1Elmt.appendChild(tdTimeseriesElmt);
            }


            let tdWhFactorElmt = document.createElement("td");
            // tdWhFactorElmt.classList.add("text-center");
            tdWhFactorElmt.classList.add("d-flex", "gap-2");

            if (tsConfig.id != null) {

                let spanTsElmt = document.createElement("span");
                spanTsElmt.innerText = tsConfig.tsId;

                let spanWhFactorElmt = document.createElement("span");
                spanWhFactorElmt.innerText = `x${tsConfig.whFactor}`;

                tdWhFactorElmt.appendChild(spanTsElmt);
                tdWhFactorElmt.appendChild(spanWhFactorElmt);
            }

            row2Elmt.appendChild(tdWhFactorElmt);
        }

        // this.#energySourceConfigElmt.appendChild(rowElmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row1Elmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row2Elmt);

    }

    #addEnergySourceConfig_OLD(energySourceConfig) {

        let row1Elmt = document.createElement("tr");
        row1Elmt.classList.add("align-middle");

        let row2Elmt = document.createElement("tr");
        row2Elmt.classList.add("align-middle");

        let thElmt = document.createElement("th");
        thElmt.classList.add("text-center", "text-break");
        thElmt.setAttribute("scope", "row");
        thElmt.setAttribute("rowspan", "2");
        thElmt.innerText = energySourceConfig.name;
        row1Elmt.appendChild(thElmt);

        for (let [energyUseId, tsConfig] of Object.entries(energySourceConfig.energyUses)) {

            let tdTimeseriesElmt = document.createElement("td");
            tdTimeseriesElmt.classList.add("text-center");

            let inputGroupTimeseriesElmt = document.createElement("div");
            inputGroupTimeseriesElmt.classList.add("input-group", "input-group-sm");

            let btnModalTimeseriesSelectorElmt = document.createElement("button");
            // btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-sm", "btn-outline-secondary");
            btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-outline-secondary");
            btnModalTimeseriesSelectorElmt.setAttribute("data-bs-toggle", "modal");
            btnModalTimeseriesSelectorElmt.setAttribute("data-bs-target", "#selectTimeseries");
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-id", energySourceConfig.sourceId);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-id", energyUseId);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-name", energySourceConfig.sourceName);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-name", tsConfig.energyUseName);
            btnModalTimeseriesSelectorElmt.id = `tsModalBtn-${energySourceConfig.sourceId}-${energyUseId}`;
            btnModalTimeseriesSelectorElmt.innerText = "...";

            let selectedTimeseriesElmt = document.createElement("div");
            // selectedTimeseriesElmt.classList.add("border", "rounded-start", "px-2");
            selectedTimeseriesElmt.classList.add("input-group-text", "bg-white");
            selectedTimeseriesElmt.setAttribute("aria-label", "Selected timeseries");
            selectedTimeseriesElmt.setAttribute("aria-describedby", btnModalTimeseriesSelectorElmt.id);
            selectedTimeseriesElmt.id = `selectedTs-${energySourceConfig.sourceId}-${energyUseId}`;
            selectedTimeseriesElmt.innerText = tsConfig.tsId;

            inputGroupTimeseriesElmt.appendChild(selectedTimeseriesElmt);

            inputGroupTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);

            // tdTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);
            tdTimeseriesElmt.appendChild(inputGroupTimeseriesElmt);

            row1Elmt.appendChild(tdTimeseriesElmt);



            let tdWhFactorElmt = document.createElement("td");
            // tdWhFactorElmt.classList.add("text-center");

            let inputGroupWhFactorElmt = document.createElement("div");
            inputGroupWhFactorElmt.classList.add("input-group", "input-group-sm");

            let spanWhFactorElmt = document.createElement("span");
            spanWhFactorElmt.classList.add("input-group-text");
            spanWhFactorElmt.id = `whFactorLabel-${energySourceConfig.sourceId}-${energyUseId}`;
            spanWhFactorElmt.innerText = "Wh factor";

            let inputWhFactorElmt = document.createElement("input");
            inputWhFactorElmt.setAttribute("type", "number");
            inputWhFactorElmt.setAttribute("aria-label", spanWhFactorElmt.id);
            // inputWhFactorElmt.classList.add("form-control", "form-control-sm");
            inputWhFactorElmt.classList.add("form-control");
            inputWhFactorElmt.id = `whFactor-${energySourceConfig.sourceId}-${energyUseId}`;
            inputWhFactorElmt.value = tsConfig.whFactor;

            // let labelWhFactorElmt = document.createElement("label");
            // labelWhFactorElmt.setAttribute("for", inputWhFactorElmt.id);
            // labelWhFactorElmt.classList.add("form-label");
            // labelWhFactorElmt.innerText = "Wh factor";

            inputGroupWhFactorElmt.appendChild(spanWhFactorElmt);
            inputGroupWhFactorElmt.appendChild(inputWhFactorElmt);

            // // tdWhFactorElmt.appendChild(labelWhFactorElmt);
            // tdWhFactorElmt.appendChild(inputWhFactorElmt);
            tdWhFactorElmt.appendChild(inputGroupWhFactorElmt);

            row2Elmt.appendChild(tdWhFactorElmt);
        }

        // this.#energySourceConfigElmt.appendChild(rowElmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row1Elmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row2Elmt);

    }

    #addEnergySource(energySource) {

        let row1Elmt = document.createElement("tr");
        row1Elmt.classList.add("align-middle");

        let row2Elmt = document.createElement("tr");
        row2Elmt.classList.add("align-middle");

        let thElmt = document.createElement("th");
        thElmt.classList.add("text-center", "text-break");
        thElmt.setAttribute("scope", "row");
        thElmt.setAttribute("rowspan", "2");
        thElmt.innerText = energySource.name;
        row1Elmt.appendChild(thElmt);

        for (let energyUse of this.#energyUses) {

            let tdTimeseriesElmt = document.createElement("td");
            tdTimeseriesElmt.classList.add("text-center");

            let inputGroupTimeseriesElmt = document.createElement("div");
            inputGroupTimeseriesElmt.classList.add("input-group", "input-group-sm");

            let btnModalTimeseriesSelectorElmt = document.createElement("button");
            // btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-sm", "btn-outline-secondary");
            btnModalTimeseriesSelectorElmt.classList.add("btn", "btn-outline-secondary");
            btnModalTimeseriesSelectorElmt.setAttribute("data-bs-toggle", "modal");
            btnModalTimeseriesSelectorElmt.setAttribute("data-bs-target", "#selectTimeseries");
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-id", energySource.id);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-id", energyUse.id);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-source-name", energySource.name);
            btnModalTimeseriesSelectorElmt.setAttribute("data-energy-use-name", energyUse.name);
            btnModalTimeseriesSelectorElmt.id = `tsModalBtn-${energySource.id}-${energyUse.id}`;
            btnModalTimeseriesSelectorElmt.innerText = "...";

            let selectedTimeseriesElmt = document.createElement("div");
            // selectedTimeseriesElmt.classList.add("border", "rounded-start", "px-2");
            selectedTimeseriesElmt.classList.add("input-group-text", "bg-white");
            selectedTimeseriesElmt.setAttribute("aria-label", "Selected timeseries");
            selectedTimeseriesElmt.setAttribute("aria-describedby", btnModalTimeseriesSelectorElmt.id);
            selectedTimeseriesElmt.id = `selectedTs-${energySource.id}-${energyUse.id}`;
            selectedTimeseriesElmt.innerText = "none";

            inputGroupTimeseriesElmt.appendChild(selectedTimeseriesElmt);

            inputGroupTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);

            // tdTimeseriesElmt.appendChild(btnModalTimeseriesSelectorElmt);
            tdTimeseriesElmt.appendChild(inputGroupTimeseriesElmt);

            row1Elmt.appendChild(tdTimeseriesElmt);



            let tdWhFactorElmt = document.createElement("td");
            // tdWhFactorElmt.classList.add("text-center");

            let inputGroupWhFactorElmt = document.createElement("div");
            inputGroupWhFactorElmt.classList.add("input-group", "input-group-sm");

            let spanWhFactorElmt = document.createElement("span");
            spanWhFactorElmt.classList.add("input-group-text");
            spanWhFactorElmt.id = `whFactorLabel-${energySource.id}-${energyUse.id}`;
            spanWhFactorElmt.innerText = "Wh factor";

            let inputWhFactorElmt = document.createElement("input");
            inputWhFactorElmt.setAttribute("type", "number");
            inputWhFactorElmt.setAttribute("aria-label", spanWhFactorElmt.id);
            // inputWhFactorElmt.classList.add("form-control", "form-control-sm");
            inputWhFactorElmt.classList.add("form-control");
            inputWhFactorElmt.id = `whFactor-${energySource.id}-${energyUse.id}`;
            inputWhFactorElmt.value = 1;

            // let labelWhFactorElmt = document.createElement("label");
            // labelWhFactorElmt.setAttribute("for", inputWhFactorElmt.id);
            // labelWhFactorElmt.classList.add("form-label");
            // labelWhFactorElmt.innerText = "Wh factor";

            inputGroupWhFactorElmt.appendChild(spanWhFactorElmt);
            inputGroupWhFactorElmt.appendChild(inputWhFactorElmt);

            // // tdWhFactorElmt.appendChild(labelWhFactorElmt);
            // tdWhFactorElmt.appendChild(inputWhFactorElmt);
            tdWhFactorElmt.appendChild(inputGroupWhFactorElmt);

            row2Elmt.appendChild(tdWhFactorElmt);
        }

        // this.#energySourceConfigElmt.appendChild(rowElmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row1Elmt);
        this.#dashboardConfigTableBodyElmt.appendChild(row2Elmt);

    }

//     #getEditBtnHTML(type, id, tab=null) {
//         if (signedUser.is_admin) {
//             let editUrlParams = {type: type, id: id};
//             if (tab != null) {
//                 editUrlParams["tab"] = tab;
//             }
//             try {
//                 let editUrl = flaskES6.urlFor(`structural_elements.edit`, editUrlParams);
//                 return `<a class="btn btn-sm btn-outline-primary text-nowrap" href="${editUrl}" role="button" title="Edit ${type}"><i class="bi bi-pencil"></i> Edit</a>`;
//             }
//             catch (error) {
//                 console.error(error);
//             }
//         }
//         return ``;
//     }

//     #getGeneralHTML(data, path) {
//         return `<div class="d-flex justify-content-between align-items-start gap-3 mb-3">
//     <div>
//         <h5 class="text-break">${data.structural_element.name}</h5>
//         <h6 class="text-break">${path}</h6>
//     </div>
//     ${this.#getEditBtnHTML(data.type, data.structural_element.id)}
// </div>
// <p class="fst-italic text-muted text-break">${data.structural_element.description}</p>
// <div class="row">
//     <dl class="col">
//         <dt>IFC ID</dt>
//         <dd>${(data.structural_element.ifc_id != null && data.structural_element.ifc_id != "") ? data.structural_element.ifc_id : "-"}</dd>
//     </dl>
// </div>`;
//     }

//     #getItemHelpHTML(itemDescription, withSpace = true) {
//         let ret = ``;
//         if (itemDescription?.length > 0) {
//             let abbrElmt = document.createElement("abbr");
//             abbrElmt.title = itemDescription != null ? itemDescription : "";
//             let abbrContentElmt = document.createElement("i");
//             abbrContentElmt.classList.add("bi", "bi-question-diamond");
//             abbrElmt.appendChild(abbrContentElmt);
//             ret = `<sup${withSpace ? ` class="ms-1"`: ``}>${abbrElmt.outerHTML}</sup>`;
//         }
//         return ret;
//     }

//     #getPropertiesHTML(data, id) {
//         let propertyDataHTML = ``;
//         if (data.properties.length > 0) {
//             for (let property of data.properties) {
//                 let unitSymbol = (property.unit_symbol != null && property.unit_symbol.length > 0) ? `<small class="text-muted ms-1">[${property.unit_symbol}]</small>` : ``;
//                 propertyDataHTML += `<dl>
//     <dt>${property.name}${unitSymbol}${this.#getItemHelpHTML(property.description)}</dt>
//     <dd>${(property.value !== "" && property.value != null) ? property.value : "-"}</dd>
// </dl>`;
//             }
//         }
//         else {
//             propertyDataHTML = `<p class="fst-italic">No data</p>`;
//         }

//         return `<div class="d-flex justify-content-between align-items-start mb-3">
//     <div class="d-flex gap-4">
//         ${propertyDataHTML}
//     </div>
//     ${this.#getEditBtnHTML(data.type, id, "properties")}
// </div>`;
//     }

//     #getTimeseriesHTML(data, id) {
//         let contentHTML = ``;
//         if (data.timeseries.length > 0) {
//             contentHTML += `<p class="text-muted text-end">Items count: ${data.timeseries.length}</p>`;
//             for (let ts_data of data.timeseries) {
//                 let unitSymbol = (ts_data.unit_symbol != null && ts_data.unit_symbol.length > 0) ? `<small class="text-black text-opacity-50">[${ts_data.unit_symbol}]</small>` : ``;
//                 contentHTML += `<li class="d-flex gap-1"><i class="bi bi-clock-history"></i><span class="fw-bold text-break">${ts_data.name}</span>${unitSymbol}${this.#getItemHelpHTML(ts_data.description, false)}</li>`;
//             }
//         }
//         else {
//             contentHTML = `<p class="fst-italic">No data</p>`;
//         }

//         return `<ul class="list-unstyled mb-3">
//     ${contentHTML}
// </ul>`;
//     }

//     #getErrorHTML(error) {
//         return `<div class="alert alert-danger" role="alert">
//     <i class="bi bi-x-octagon me-2"></i>
//     ${error}
// </div>`;
//     }

//     #renderNoData() {
//         this.#generalTabContentElmt.innerHTML = "";
//         this.#propertiesTabContentElmt.innerHTML = "";
//     }

//     #renderGeneral(id, type, path) {
//         this.#generalTabContentElmt.innerHTML = "";
//         this.#generalTabContentElmt.appendChild(new Spinner());

//         if (this.#generalReqID != null) {
//             this.#internalAPIRequester.abort(this.#generalReqID);
//             this.#generalReqID = null;
//         }
//         this.#generalReqID = this.#internalAPIRequester.get(
//             flaskES6.urlFor(`api.structural_elements.retrieve_data`, {type: type, id: id}),
//             (data) => {
//                 this.#generalTabContentElmt.innerHTML = this.#getGeneralHTML(data, path);
//             },
//             (error) => {
//                 this.#generalTabContentElmt.innerHTML = this.#getErrorHTML(error.message);
//             },
//         );
//     }

//     #renderProperties(id, type, path) {
//         this.#propertiesTabContentElmt.innerHTML = "";
//         this.#propertiesTabContentElmt.appendChild(new Spinner());

//         if (this.#propertiesReqID != null) {
//             this.#internalAPIRequester.abort(this.#propertiesReqID);
//             this.#propertiesReqID = null;
//         }
//         this.#propertiesReqID = this.#internalAPIRequester.get(
//             flaskES6.urlFor(`api.structural_elements.retrieve_property_data`, {type: type, id: id}),
//             (data) => {
//                 this.#propertiesTabContentElmt.innerHTML = this.#getPropertiesHTML(data, id);
//             },
//             (error) => {
//                 this.#propertiesTabContentElmt.innerHTML = this.#getErrorHTML(error.message);
//             },
//         );
//     }

//     #renderTimeseries(id, type, path) {
//         this.#timeseriesTabContentElmt.innerHTML = "";
//         this.#timeseriesTabContentElmt.appendChild(new Spinner());

//         if (this.#tsReqID != null) {
//             this.#internalAPIRequester.abort(this.#tsReqID);
//             this.#tsReqID = null;
//         }
//         this.#tsReqID = this.#internalAPIRequester.get(
//             flaskES6.urlFor(`api.structural_elements.retrieve_timeseries`, {type: type, id: id}),
//             (data) => {
//                 this.#timeseriesTabContentElmt.innerHTML = this.#getTimeseriesHTML(data, id);
//             },
//             (error) => {
//                 this.#timeseriesTabContentElmt.innerHTML = this.#getErrorHTML(error.message);
//             },
//         );
//     }

    // render(id, type, path, name) {
    //     // this.#selectedItemsPerTab[this.#tabSitesSelected.id] = {id: id, type: type, path: path};
    //     // for (let tabElmt of this.#tabPropertiesElmts) {
    //     //     this.#alreadyLoadedPerTab[tabElmt.id] = false;
    //     // }
    //     // this.refresh();

    //     console.log("render");
    //     console.log(id);
    //     console.log(type);
    //     console.log(path);
    //     console.log(name);

    //     let viewUrl = flaskES6.urlFor(`dashboards.energy_consumption.view`, {structural_element_type: type, structural_element_id: id});
    //     this.#dashboardSetupBtnElmt.href = viewUrl;
    //     this.#dashboardSetupBtnElmt.classList.remove("d-none");

    //     // Get dashboard data.
    // }

    refresh() {
        // let selectedItemData = this.#selectedItemsPerTab[this.#tabSitesSelected.id];
        // if (selectedItemData != null) {
        //     if (!this.#alreadyLoadedPerTab[this.#tabPropertiesSelected.id]) {
        //         this.#renderPerTab[this.#tabPropertiesSelected.id]?.call(this, selectedItemData.id, selectedItemData.type, selectedItemData.path);
        //         this.#alreadyLoadedPerTab[this.#tabPropertiesSelected.id] = true;
        //     }
        // }
        // else {
        //     this.#renderNoData();
        // }
    }
}
