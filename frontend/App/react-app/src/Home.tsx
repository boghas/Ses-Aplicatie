import React, { useEffect, useState } from "react";
import api from "./api";

interface ClientData {
  client_id: number;
  client_name: string;
}

const Home: React.FC = () => {
  const [data, setData] = useState<ClientData[]>([]);

  useEffect(()=> {
    api.get<ClientData[]>(`${import.meta.env.VITE_API_URL}/`)
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="container mt-5">
      <table className="table">
        <thead>
          <tr>
            <th>client_id</th>
            <th>client_name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((d, i)=> (
            <tr key={i}>
              <td>{d.client_id}</td>
              <td>{d.client_name}</td>
              <td>
                <a href={`/detalii/${d.client_id}`} >Detalii</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Home;