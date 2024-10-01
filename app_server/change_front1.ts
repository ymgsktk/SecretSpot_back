const FetchScholarInfo = async (DepPoint: string, DepartureTime: number, ArrivalTime: number, Budget: number) => {
	try {
		// POSTメソッドを使用し、リクエストボディにパラメータを含める
        const URL = "http://localhost:8080";
		const response = await fetch(`${URL}/api/execute`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			// クエリパラメータをリクエストボディとして送信
			body: JSON.stringify({
				DepPoint: DepPoint,
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

export default FetchScholarInfo;
