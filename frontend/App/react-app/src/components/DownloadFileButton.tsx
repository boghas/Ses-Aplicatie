import React from "react";
import api from "../api";

interface DownloadFileButtonProps {
  client_id: number;
  endpoint: string;
  file_names: string;
}

const DownloadFileButton: React.FC<DownloadFileButtonProps> = ({ client_id, endpoint, file_names }) => {
  const handleDownload = () => {
    console.log("Download button clicked");
  
    // Split the file_names string into an array of filenames
    const filenames = file_names.split(',');
    console.log(filenames)
  
    // Iterate over each filename to download the corresponding file
    filenames.forEach((filename, index) => {
      const url = `${import.meta.env.VITE_API_URL}/${endpoint}/${client_id}?file_name=${new URLSearchParams(filename).toString()}`;
      api.get(url, {
        responseType: 'blob',
        data: filename,
      })
      .then(response => {
        let downloadedFilename = filename.trim(); // Trim whitespace from filename
  
        // Extract filename from content-disposition header
        const contentDisposition = response.headers['content-disposition'];
        if (contentDisposition) {
          const matches = contentDisposition.match(/filename="(.+)"/);
          if (matches && matches.length > 1) {
            downloadedFilename = matches[1];
          }
        }
  
        const url = window.URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', downloadedFilename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link); // Clean up after download
  
        // Log success message for each file downloaded
        console.log(`File ${index + 1} downloaded: ${downloadedFilename}`);
      })
      .catch(error => {
        console.error('Error downloading file:', error);
      });
      alert("Fisier/Fisiere descarcate cu success!");
    });
  };

  return (
    <button onClick={handleDownload}>Download</button>
  );
};

export default DownloadFileButton;