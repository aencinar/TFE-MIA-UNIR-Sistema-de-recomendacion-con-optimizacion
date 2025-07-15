
export type RequestConfig = {
	headers: Record<string, string>;
}

export type ParametersToRequest<T> = {
	url: string,
	method: 'GET' | 'POST';
	headers?: Record<string, string>;
	body?: any;
	onSuccess: (data: { [key: string]: any }) => T | Error;
	onFailure: (data: Error) => T | Error;
};

export type RequestOptions = {
	method: 'GET' | 'POST';
	headers?: Record<string, string>;
	body?: any;
};

export type Request = {
	url: string;
	requestOptions: RequestOptions;
};

export type SuccessResponse = {
	ok: boolean;
	data: any;
};

export type ErrorResponse = {
	ok: boolean;
	data: Error;
};
