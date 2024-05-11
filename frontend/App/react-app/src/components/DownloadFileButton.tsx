import React from "react";
import axios from 'axios';

interface DownloadFileButtonProps {
  client_id: number;
  endpoint: string;
}

const DownloadFileButton: React.FC<DownloadFileButtonProps> = ({ client_id, endpoint }) => {
  const handleDownload = () => {
    console.log("Download button clicked"); // Add this line

    axios.get(`http://localhost:8000/${endpoint}/${client_id}`, {
      responseType: 'blob',
    })
    .then(response => {
      let filename = `file_${client_id}.pdf`; // Default filename if not found
      console.log(response)

      // Extract filename from content-disposition header
      const contentDisposition = response.headers['content-disposition'];
      if (contentDisposition) {
        const matches = contentDisposition.match(/filename="(.+)"/);
        if (matches && matches.length > 1) {
          filename = matches[1];
        }
      }

      const url = window.URL.createObjectURL(response.data); // Access response.data directly here
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Clean up after download
    })
    .catch(error => {
      console.error('Error downloading file:', error);
    });
  };

  return (
    <button onClick={handleDownload}>Download</button>
  );
};

export default DownloadFileButton;