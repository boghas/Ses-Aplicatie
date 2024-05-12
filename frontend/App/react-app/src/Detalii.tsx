import React, { useEffect, useState } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';
import DownloadFileButton from "./components/DownloadFileButton";
import UploadFileButton from "./components/UploadFileButton";

interface ClientData {
  client_id: number;
  client_name: string;
  documente_incarcate: string;
  contract_anexa: string;
  factura_avans: string;
  serie_inventor: string;
  serie_smart_meter: string;
  serie_panouri: string;
  dosar_prosumator: string;
  garantii_client: string;
}

const Detalii: React.FC = () => {
  const [data, setData] = useState<ClientData>({
    client_id: 0,
    client_name: "",
    documente_incarcate: "",
    contract_anexa: "",
    factura_avans: "",
    serie_inventor: "",
    serie_smart_meter: "",
    serie_panouri: "",
    dosar_prosumator: "",
    garantii_client: ""
  });
  const { client_id } = useParams<{ client_id: string }>();

  useEffect(()=> {
    axios.get<ClientData>(`http://localhost:8000/client/${client_id}`)
      .then(res => setData(res.data))
      .catch(err => console.log(err));
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
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_documente_incarcate"} file_type={"document"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="documente_incarcate" /></td>
          </tr>
          <tr>
            <td>Contract Anexa: {data.contract_anexa}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_contract_anexa"} file_type={"contract"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="contract_anexa" /></td>
          </tr>
          <tr>
            <td>Factura Avans: {data.factura_avans}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_factura_avans"} file_type={"factura"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="factura_avans" /></td>
          </tr>
          <tr>
            <td>Serie Inventor: {data.serie_inventor}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_inventor"} file_type={"new_serie_inventor"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_inventor" /></td>
          </tr>
          <tr>
            <td>Serie Smart Meter: {data.serie_smart_meter}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_smart_meter"} file_type={"new_serie_smart_meter"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_smart_meter" /></td>
          </tr>
          <tr>
            <td>Serie Panouri: {data.serie_panouri}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_panouri"} file_type={"serie_panouri"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_panouri" /></td>
          </tr>
          <tr>
            <td>Dosar Prosumator: {data.dosar_prosumator}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_dosar_prosumator"} file_type={"dosar"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="dosar_prosumator" /></td>
          </tr>
          <tr>
            <td>Garantii Client: {data.garantii_client}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_garantii_client"} file_type={"garantii"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="garantii_client" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Detalii;
