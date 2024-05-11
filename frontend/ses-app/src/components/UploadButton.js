import React from 'react';
import axios from 'axios';

class UploadFileButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null
        };
    }

    handleFileChange = (event) => {
        this.setState({ selectedFile: event.target.files[0] });
    };

    handleFileUpload = async () => {
        try {
            const { selectedFile } = this.state;
            const { client_id, endpoint } = this.props;
    
            if (!selectedFile) {
                console.log('No file selected');
                return;
            }
    
            const formData = new FormData();
            formData.append('file', selectedFile); // 'file' key is important, should match backend
    
            const response = await fetch(`http://localhost:8000/${endpoint}/${client_id}`, {
            method: "POST",
            body: formData,
            });
    
            console.log('File uploaded successfully:', response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    render() {
        return (
            <div>
                <input type="file" onChange={this.handleFileChange} />
                <button onClick={this.handleFileUpload}>Upload File</button>
            </div>
        );
    }
}

export default UploadFileButton;