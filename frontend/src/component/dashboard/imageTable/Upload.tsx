import { UploadOutlined } from '@ant-design/icons';
import { Button, message, notification, Upload } from 'antd';
import axios from "axios"


notification.config({
    placement: 'topRight',
    duration: 3,
});

// Type definitions for the component props
interface UploadStructureProps {
    researchFieldData: { id?: number }; // Adjust this type if necessary
    freshTable: () => void;
}

const UploadStructure: React.FC<UploadStructureProps> = ({ researchFieldData, freshTable }) => {

    // Define upload props with appropriate types
    const props = {
        name: 'file',
        action: '/api/uploadOriginalImages/',
        headers: {
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            cache: false,
            domainId: (researchFieldData?.id) ?? 1
        },
        data: (file: File) => {
            console.log("file: ", file)
            let form_data = new FormData();

            form_data.append("files[]", file);
            form_data.append("name", "username");
            return {
                form_data
            }
        },
        onChange(info: { file: any; fileList: any[] }) {
            console.log("info:", info)
            if (info.file.status !== 'uploading') {
                notification.info({
                    message: 'Image uploading...',
                })
                console.log(info.file, info.fileList);
            }
            if (info.file.status === 'done') {
                notification.success({
                    message: `Image successfully uploaded.`,
                })
                message.success(`${info.file.name} file uploaded successfully`);
                freshTable();
            } else if (info.file.status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        },
    };

    return (
        //@ts-ignore
        <Upload {...props}>
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
        </Upload>


    );
}
export default UploadStructure;