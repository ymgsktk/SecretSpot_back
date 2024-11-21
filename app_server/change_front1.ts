const FetchServerInfo = async (DepPoint: string, DepAddress: string, DepartureTime: number, ArrivalTime: number, Budget: number) => {
	try {
		// POSTメソッドを使用し、リクエストボディにパラメータを含める
		//const URL = "https://038f-240f-106-d945-1-f930-a00a-efc0-b721.ngrok-free.app";
        const URL = "http://localhost:8080";

		const response = await fetch(`${URL}/api/execute`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			// クエリパラメータをリクエストボディとして送信
			body: JSON.stringify({
				DepPoint: DepPoint,
				DepAddress: DepAddress,
				DepartureTime: DepartureTime,
				ArrivalTime: ArrivalTime,
				Budget: Budget
			})
		});

		// レスポンスが正常か確認
		if (!response.ok) {
			throw new Error('情報の取得に失敗しました');
		}

		// JSONデータを取得
		const data = await response.json();
		console.log("response data: ", data);

		// データを返す
		return { data };
	} catch (error) {
		// エラーをキャッチして返す
		return { error };
	}
};

export default FetchServerInfo;
