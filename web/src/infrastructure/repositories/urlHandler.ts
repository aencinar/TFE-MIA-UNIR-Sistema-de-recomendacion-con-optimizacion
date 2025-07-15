const API_URL = "http://localhost:8000";

export function getURL(url: string): string {
	if (process.env.NODE_ENV === 'test') {
		url = `http://localhost:3000${url}`;
	}else{
		url = `${API_URL}${url}`;
	}

	return url;
}