import React from 'react';
import axios from 'axios';
import FileSaver from 'file-saver';

class DownloadFileButton extends React.Component {
    downloadFile = async () => {
        try {
            const { client_id, endpoint } = this.props;
            const response = await axios.get(`http://localhost:8000/${endpoint}/${client_id}`, {
                responseType: 'blob',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'X-Requested-With'
                }
            });

            let fileName = 'downloaded_file'; // Default filename
            if (response.headers['content-disposition']) {
                const contentDisposition = response.headers['content-disposition'];
                fileName = decodeURI(contentDisposition.split('filename*=UTF-8\'\'')[1]);
            }

            FileSaver.saveAs(response.data, fileName);
        } catch (error) {
            console.log('Error downloading file:', error);
        }
    };

    render() {
        return (
            <button onClick={this.downloadFile}>Descarca</button>
        );
    }
}

export default DownloadFileButton;