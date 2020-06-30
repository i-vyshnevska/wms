import {ScenarioBaseMixin} from "./mixins.js";
import {process_registry} from "../services/process_registry.js";
import {demotools} from "../demo/demo.core.js"; // FIXME: dev only
import {} from "../demo/demo.delivery.js"; // FIXME: dev only

export var LocationContentTransfer = Vue.component("location-content-transfer", {
    mixins: [ScenarioBaseMixin],
    template: `
        <Screen :screen_info="screen_info">
            <template v-slot:header>
                <state-display-info :info="state.display_info" v-if="state.display_info"/>
            </template>
            <searchbar
                v-if="state.on_scan"
                v-on:found="on_scan"
                :input_placeholder="search_input_placeholder"
                />
            <div v-if="state_in(['start_single', 'scan_destination']) && state.data.move_line">
                <detail-picking
                    :key="make_state_component_key(['picking'])"
                    :record="state.data.move_line.picking"
                    :options="{main: true}"
                    />
                <batch-picking-line-detail
                    :line="state.data.move_line"
                    :article-scanned="state_is('scan_destination')"
                    :show-qty-picker="state_is('scan_destination')"
                    />
            </div>
            <div v-if="state_is('scan_destination_all')">
                <item-detail-card
                    v-for="move_line in state.data.move_lines"
                    :key="make_state_component_key(['detail-move-line', move_line.id])"
                    :record="move_line"
                    :options="move_line_detail_list_options(move_line)"
                    />
            </div>
            <div class="button-list button-vertical-list full">
                <v-row align="center" v-if="state_is('scan_destination_all')">
                    <v-col class="text-center" cols="12">
                        <btn-action @click="state.on_split_by_line">Split by line</btn-action>
                    </v-col>
                </v-row>
            </div>
        </Screen>
        `,
    // FIXME: just for dev
    // mounted: function() {
    //     // TEST force state and data
    //     const state = "select_package";
    //     const dcase = demotools.get_case(this.usage);
    //     const data = dcase["select_package"].data[state];
    //     this.state_set_data(data, state);
    //     this._state_load(state);
    // },
    methods: {
        screen_title: function() {
            if (!this.has_picking()) return this.menu_item().name;
            return this.current_picking().name;
        },
        // TODO: if we have this working we can remove the picking detail?
        current_doc: function() {
            const picking = this.current_picking();
            return {
                record: picking,
                identifier: picking.name,
            };
        },
        current_picking: function() {
            const data = this.state_get_data("start");
            if (_.isEmpty(data) || _.isEmpty(data.move_line.picking)) {
                return {};
            }
            return data.move_line.picking;
        },
        has_picking: function() {
            return !_.isEmpty(this.current_picking());
        },
        move_line_detail_list_options: function(move_line) {
            return this.utils.misc.move_line_product_detail_options(move_line, {
                fields_blacklist: ["product.qty_available"],
            });
        },
    },
    data: function() {
        const self = this;
        return {
            usage: "location_content_transfer",
            initial_state_key: "start",
            states: {
                init: {
                    enter: () => {
                        this.state_reset_data();
                        this.wait_call(this.odoo.call("start_or_recover"));
                    },
                },
                start: {
                    display_info: {
                        scan_placeholder: "Scan pack / product / lot",
                    },
                    on_scan: scanned => {
                        this.wait_call(this.odoo.call("TODO", {barcode: scanned.text}));
                    },
                },
                scan_location: {
                    display_info: {
                        title: "Start by scanning a location",
                        scan_placeholder: "Scan location",
                    },
                    on_scan: scanned => {
                        this.wait_call(this.odoo.call("TODO", {barcode: scanned.text}));
                    },
                },
                scan_destination_all: {
                    display_info: {
                        title: "Scan destination location for all items",
                        scan_placeholder: "Scan location",
                    },
                    on_scan: scanned => {
                        this.wait_call(
                            this.odoo.call("set_destination_all", {
                                barcode: scanned.text,
                            })
                        );
                    },
                    on_split_by_line: () => {
                        const location = this.state.data.move_lines[0].location_src;
                        this.wait_call(
                            this.odoo.call("go_to_single", {location_id: location.id})
                        );
                    },
                },
                start_single: {
                    display_info: {
                        scan_placeholder: "Scan pack / product / lot",
                    },
                    on_scan: scanned => {
                        let endpoint, endpoint_data;
                        const data = this.state.data;
                        if (data.package_level) {
                            endpoint = "scan_package";
                            endpoint_data = {
                                package_level_id: data.package_level.id,
                                location_id: data.package_level.location_src.id,
                                barcode: scanned.text,
                            };
                        } else {
                            endpoint = "scan_line";
                            endpoint_data = {
                                move_line_id: data.move_line.id,
                                location_id: data.move_line.location_src.id,
                                barcode: scanned.text,
                            };
                        }
                        this.wait_call(this.odoo.call(endpoint, endpoint_data));
                    },
                },
                scan_destination: {
                    enter: () => {
                        this.reset_notification();
                    },
                    display_info: {
                        title: "Set a qty and scan destination location",
                        scan_placeholder: "Scan location",
                    },
                    events: {
                        qty_edit: "on_qty_update",
                    },
                    on_qty_update: qty => {
                        this.state.data.destination_qty = qty;
                    },
                    on_scan: scanned => {
                        let endpoint, endpoint_data;
                        const data = this.state.data;
                        if (data.package_level) {
                            endpoint = "set_destination_package";
                            endpoint_data = {
                                package_level_id: data.package_level.id,
                                location_id: data.package_level.location_src.id,
                                barcode: scanned.text,
                            };
                        } else {
                            endpoint = "set_destination_line";
                            endpoint_data = {
                                move_line_id: data.move_line.id,
                                location_id: data.move_line.location_src.id,
                                barcode: scanned.text,
                                quantity:
                                    this.state.data.destination_qty ||
                                    data.move_line.quantity,
                            };
                        }
                        this.wait_call(this.odoo.call(endpoint, endpoint_data));
                    },
                    on_split_by_line: () => {
                        const location = this.state.data.move_lines[0].location_src;
                        this.wait_call(
                            this.odoo.call("go_to_single", {location_id: location.id})
                        );
                    },
                },
            },
        };
    },
});

process_registry.add("location_content_transfer", LocationContentTransfer);
