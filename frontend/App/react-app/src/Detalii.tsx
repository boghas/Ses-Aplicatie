import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import DownloadFileButton from "./components/DownloadFileButton";
import UploadFileButton from "./components/UploadFileButton";
import api from "./api";

interface ClientData {
  client_id: number;
  client_name: string;
  documente_incarcate: string;
  contract_si_anexa: string;
  factura_avans: string;
  serie_inventor: string;
  serie_smart_meter: string;
  serie_panouri: string;
  dosar_prosumator: string;
  certificat_racordare: string;
  garantii_client: string;
  documente_incarcate_nume_fisier: string;
  contract_si_anexa_nume_fisier: string;
  factura_avans_nume_fisier: string;
  serie_inventor_nume_fisier: string;
  serie_smart_meter_nume_fisier: string;
  serie_panouri_nume_fisier: string;
  dosar_prosumator_nume_fisier: string;
  certificat_racordare_nume_fisier: string;
  garantii_client_nume_fisier: string;
}

const Detalii: React.FC = () => {
  const [data, setData] = useState<ClientData>({
    client_id: 0,
    client_name: "",
    documente_incarcate: "",
    contract_si_anexa: "",
    factura_avans: "",
    serie_inventor: "",
    serie_smart_meter: "",
    serie_panouri: "",
    dosar_prosumator: "",
    certificat_racordare: "",
    garantii_client: "",
    documente_incarcate_nume_fisier: "",
    contract_si_anexa_nume_fisier: "",
    factura_avans_nume_fisier: "",
    serie_inventor_nume_fisier: "",
    serie_smart_meter_nume_fisier: "",
    serie_panouri_nume_fisier: "",
    dosar_prosumator_nume_fisier: "",
    certificat_racordare_nume_fisier: "",
    garantii_client_nume_fisier: ""
  });
  const { client_id } = useParams<{ client_id: string }>();

  useEffect(()=> {
    api.get<ClientData>(`http://localhost:8000/client/${client_id}`)
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, [client_id]);

  return (
    <div className="container mt-5">
      <h1>Client: {data.client_id}: {data.client_name}</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Incarca</th>
            <th>Descarca</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Documente Incarcate: {data.documente_incarcate}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_documente_incarcate"} file_type={"document"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="documente_incarcate" file_names={data.documente_incarcate_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Contract Anexa: {data.contract_si_anexa}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_contract_anexa"} file_type={"contract_anexa"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="contract_anexa" file_names={data.contract_si_anexa_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Factura Avans: {data.factura_avans}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_factura_avans"} file_type={"factura"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="factura_avans" file_names={data.factura_avans_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Serie Inventor: {data.serie_inventor}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_inventor"} file_type={"new_serie_inventor"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_inventor" file_names={data.serie_inventor_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Serie Smart Meter: {data.serie_smart_meter}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_smart_meter"} file_type={"new_serie_smart_meter"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_smart_meter" file_names={data.serie_smart_meter_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Serie Panouri: {data.serie_panouri}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_serie_panouri"} file_type={"serie_panouri"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="serie_panouri" file_names={data.serie_panouri_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Dosar Prosumator: {data.dosar_prosumator}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_dosar_prosumator"} file_type={"dosar"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="dosar_prosumator"  file_names={data.dosar_prosumator_nume_fisier} /></td>
          </tr>
          <tr>
            <td>Certificat Racordare: {data.certificat_racordare}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_certificat_racordare"} file_type={"new_certificat_racordare"} /></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="certificat_racordare"  file_names={data.certificat_racordare_nume_fisier} /></td>
          </tr>
            <tr>
            <td>Garantii Client: {data.garantii_client}</td>
            <td><UploadFileButton client_id={data.client_id} endpoint={"upload_garantii_client"} file_type={"garantii"}/></td>
            <td><DownloadFileButton client_id={data.client_id} endpoint="garantii_client" file_names={data.garantii_client_nume_fisier}/></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Detalii;
