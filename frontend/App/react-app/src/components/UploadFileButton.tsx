import { useState } from 'react';
import api from '../api';

interface UploadButtonProps {
  client_id: number;
  endpoint: string;
  file_type: string;
}

const UploadButton: React.FC<UploadButtonProps> = ({ client_id, endpoint, file_type }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const uploadFile = async () => {
    if (!selectedFiles.length) return;

    const formData = new FormData();
    selectedFiles.forEach(selectedFile => {
      formData.append(file_type, selectedFile);
    });

    try {
      const response = await api.put(`${import.meta.env.VITE_API_URL}/${endpoint}/${client_id}`, formData, {
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
