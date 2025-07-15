import { buildResponseError, responseHandler } from './handler';
import { SuccessResponse, ErrorResponse, Request } from './types';
import { http } from "./http";


export async function callRequest(request: Request): Promise<SuccessResponse | ErrorResponse> {
	const { url, requestOptions } = request;
	let response: Promise<Response>;
	const methodType = requestOptions.method.toLowerCase()

	response = http[methodType as keyof typeof http](url, requestOptions);

	return response.then(responseHandler).catch(buildResponseError);
}