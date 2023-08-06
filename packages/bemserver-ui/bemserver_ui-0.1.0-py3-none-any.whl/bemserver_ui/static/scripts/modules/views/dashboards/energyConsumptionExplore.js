import { InternalAPIRequest } from "../../tools/fetcher.js";
import { flaskES6, signedUser } from "../../../app.js";
import { Spinner } from "../../components/spinner.js";


export class EnergyConsumptionExploreView {

    #internalAPIRequester = null;
    // #generalReqID = null;
    // #propertiesReqID = null;
    // #tsReqID = null;

    #dashboardSetupBtnElmt = null;

    constructor() {
        this.#cacheDOM();
        this.#initEventListeners();

        this.#internalAPIRequester = new InternalAPIRequest();
    }

    #cacheDOM() {
        this.#dashboardSetupBtnElmt = document.getElementById("dashboardSetupBtn");
    }

    #initEventListeners() {
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

    render(id, type, path, name) {
        // this.#selectedItemsPerTab[this.#tabSitesSelected.id] = {id: id, type: type, path: path};
        // for (let tabElmt of this.#tabPropertiesElmts) {
        //     this.#alreadyLoadedPerTab[tabElmt.id] = false;
        // }
        // this.refresh();

        console.log("render");
        console.log(id);
        console.log(type);
        console.log(path);
        console.log(name);

        let viewUrl = flaskES6.urlFor(`dashboards.energy_consumption.config`, {structural_element_type: type, structural_element_id: id});
        this.#dashboardSetupBtnElmt.href = viewUrl;
        this.#dashboardSetupBtnElmt.classList.remove("d-none");

        // Get dashboard data.
    }

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
