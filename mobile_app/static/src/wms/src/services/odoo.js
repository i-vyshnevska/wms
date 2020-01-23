export class Odoo {

    constructor(params) {
        this.params = params;
        this.process_name = this.params.process_name;
        this.process_menu = this.params.process_menu;
        // FIXME: get a real one from input
        this.api_key = '72B044F7AC780DAC'
    }

    _call(endpoint, method, data) {
        console.log('CALL', endpoint);
        let params = {
            method: method,
            headers: this._get_headers()
        }
        if (data !== undefined) {
            if (method == 'GET') {
                endpoint += new URLSearchParams(data).toString();
            } else if (method == 'POST') {
                params[body] = JSON.stringify(data);
            }
        }
        fetch(
            this._get_url(endpoint), params
        )
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    _get_headers() {
        return {
            'Content-Type': 'application/json',
            'SERVICE_CTX_PROCESS_NAME': this.process_name,
            'SERVICE_CTX_PROCESS_MENU': this.process_menu,
            'HTTP_API_KEY': this.api_key,
        }
    }

    _get_url (endpoint) {
        return 'http://localhost:8069/shopfloor/' + this.process_name + '/' + endpoint;
    }
    fetchOperation (barcode) {
        return this._call('start', 'GET', {'barcode': barcode})
    }
    validate (operation, confirmed) {
        console.log('Validate', operation);
        let data = {
            'id': operation.id, 'location_barcode': operation.location_barcode
        }
        if (confirmed !== undefined)
            data['confirmed'] = true;
        return this._call('validate', 'POST', data)
    }
    cancelMove (id) {}
    validateMove (id) {}

    scanLocation (barcode) {
        return this._call('scan_location', 'GET', {'barcode': barcode})
    }

}

