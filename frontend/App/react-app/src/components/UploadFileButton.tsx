import { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const UploadButton = ({ client_id, endpoint, file_type}) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const nav = useNavigate()

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const uploadFile = async () => {
    if (!selectedFiles) return;

    const formData = new FormData();
    selectedFiles.forEach(selectedFile => {
      formData.append(file_type, selectedFile);
    })
    

    try {
        const response = await api.put(`http://localhost:8000/${endpoint}/${client_id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data); // Assuming the response contains some data
      alert("Fisier/Fisiere incarcate cu success!");
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} multiple />
      <button type="button" onClick={uploadFile}>Upload</button>
    </div>
  );
};

export default UploadButton;