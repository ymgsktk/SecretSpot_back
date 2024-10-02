import { useEffect, useState } from 'react';
import FetchServerInfo from '../change_front1';  // FetchScholarInfoのインポート

function Home() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // サンプルデータでAPIを呼び出す
    async function fetchData() {
      try {
        const DepPoint = { lat: 35.6586, lng: 139.7454 };  // DepPointとして緯度と経度を設定
        const DepAddress = "1-1 Marunouchi, Chiyoda City, Tokyo";  // 出発地点の住所
        const DepartureTime = { hour: 10, min: 30 };  // 出発時刻を設定
        const ArrivalTime = { hour: 12, min: 45 };  // 到着時刻を設定
        const Budget = 100;  // 予算を設定

        const result = await FetchServerInfo(DepPoint, DepAddress, DepartureTime, ArrivalTime, Budget);

        if (result.error) {
          setError(result.error);
        } else {
          setData(result.data);
        }
      } catch (err) {
        setError(err.message);
      }
    }
    fetchData();
  }, []);

  return (
    <div>
      <h1>Welcome to Next.js!</h1>
      {error && <p>Error: {error}</p>}
      {data ? (
        <div>
          <h2>スポット情報:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Home;
