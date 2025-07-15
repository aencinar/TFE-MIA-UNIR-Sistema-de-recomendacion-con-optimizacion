const errorMap = {
	400: {
		errorCode: 'REQUEST_ERROR',
		message: 'BAD_REQUEST',
		result: 'ERROR',
	},
	default: {
		errorCode: 'REQUEST_ERROR',
		message: 'GENERIC_ERROR',
		result: 'ERROR',
	},
};

export function buildResponseError(errorCode: number) {
	const errorResponse = errorMap[errorCode as keyof typeof errorMap] || errorMap.default;
	return { ok: false, data: errorResponse };
}

export async function responseHandler(response: Response) {
	let data = await response.json();

	if (response.ok) return { ok: true, data };

	return buildResponseError(response.status);
}
