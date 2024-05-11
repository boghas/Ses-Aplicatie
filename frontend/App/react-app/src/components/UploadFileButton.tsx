import React, { useState } from 'react';
import axios from 'axios';

const UploadButton = ({ client_id: number, endpoint: string }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('new_serie_smart_meter', selectedFile);

    try {
      const response = await axios.put(`http://localhost:8000/${endpoint}/${client_id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data); // Assuming the response contains some data
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button type="button" onClick={uploadFile}>Upload</button>
    </div>
  );
};

export default UploadButton;