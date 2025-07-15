import { ParametersToRequest } from './http/types';
import { callRequest } from './http/request';

export function RequestProxy() {

    return {
        http: async function<T>(params: ParametersToRequest<T>) {
            const { url, method, body, headers, onFailure, onSuccess } = params;
            const request = {
                url,
                requestOptions: {
                    method, 
                    body,
                    headers
                }
            };
        
            const json = await callRequest(request);
        
            if (json.ok) {
                return onSuccess(json.data);
            }
        
            return onFailure(json.data);
        }
    }
}