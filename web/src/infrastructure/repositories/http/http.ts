import { RequestOptions } from './types';

const get = async  (endpoint: string, requestOptions? : RequestOptions): Promise<Response> => {
	const { headers } = requestOptions || {};
	const response = await fetch(endpoint, {
		method: 'GET',
		headers,
	});
	return response;
};

const post = async (endpoint: string, requestOptions : RequestOptions): Promise<Response> => {
	const { headers } = requestOptions || {};
	const response = await fetch(endpoint, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...headers,
		},
		body: JSON.stringify(requestOptions.body),
	});

	return response;
};

export const http = {
	get,
	post
};