import React, { useEffect, useState } from "react"
import axios from 'axios'
import { useParams } from 'react-router-dom';


function Detalii() {
    const [data, setData] = useState([])
    const { client_id } = useParams();

  useEffect(()=> {
    axios.get(`http://localhost:8000/client/${client_id}`)
    .then(res => setData(res.data))
    .catch(err => console.log(err))
  }, [client_id]);

    return (
        <div className="container mt-5">
          <table className="table">
            <thead>
            <tr>
                <th>Client</th>
                <th>Incarca</th>
                <th>Descarca</th>
            </tr>
            </thead>
            <tbody>
                <tr>
                    <td>ID: {data.client_id}</td>
                </tr>
                <tr>
                    <td>Nume: {data.client_name}</td>
                </tr>
                <tr>
                    <td>Documente Incarcate: {data.documente_incarcate}</td>
                    <td>
                        <button>Incarca</button>
                        </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Contract Anexa: {data.contract_anexa}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Factura Avans: {data.factura_avans}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Serie Inventor: {data.serie_invertor}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Serie Smart Meter: {data.serie_smart_meter}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Serie Panouri: {data.serie_panouri}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Dosar Prosumator: {data.dosar_prosumator}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
                <tr>
                    <td>Garantii Client: {data.garantii_client}</td>
                    <td>
                        <button>Incarca</button>
                    </td>
                    <td>
                        <button>Descarca</button>
                    </td>
                </tr>
            </tbody>
          </table>
        </div>
      )
    }
    
    export default Detalii 