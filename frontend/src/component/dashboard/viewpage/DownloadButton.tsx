import React, { useState, useEffect } from 'react'
import { Button, Modal, Form, Select, Switch } from "antd"
import axios from "axios"
import FileDownload from 'js-file-download'

export default function DownloadButton({ id }) {


    const [form] = Form.useForm();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(false)
    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setLoading(true)
        console.log("form keys:", Object.keys(form.getFieldValue()))
        console.log("form:", form.getFieldValue())
        let visual_image_value = form.getFieldValue().visualizationOverlay ? 1 : 0;
        axios({
            // Endpoint to send files
            url: "/api/exportTrainingImages/",
            method: "GET",
            responseType: 'blob', // Important
            params: {
                training_file_id: id,
                image_file_type: form.getFieldValue().imageType,
                mask_file_type: form.getFieldValue().maskType,
                visual_image_check: visual_image_value
            }
        }).then((res) => {
            console.log("/api/exportTrainingImages/", res)
            FileDownload(res.data, 'training_file.zip');
            setLoading(false)
            setIsModalOpen(false);
        }).catch((err) => { console.log(err) });

    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    useEffect(() => {

    }, [])
    return (
        <>
            <Button onClick={showModal}>Download</Button>
            <Modal title="Download Dataset" open={isModalOpen} onCancel={handleCancel}
                footer={[
                    <Button key="back" onClick={handleCancel}>
                        Cancel
                    </Button>,
                    <Button key="submit" type="primary" onClick={handleOk} loading={loading}>
                        Download
                    </Button>,
                ]}
            >
                <Form
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 14 }}
                    form={form}
                >
                    <Form.Item name="imageType" label="Image type:" initialValue={"h5"}>
                        <Select>
                            <Select.Option value="h5">HDF5</Select.Option>
                            <Select.Option value="png_16">PNG 16 Bit</Select.Option>
                            <Select.Option value="png_8">PNG 8 Bit</Select.Option>
                            <Select.Option value="jpg">JPG</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="maskType" label="Mask type:" initialValue={"h5"}>
                        <Select>
                            <Select.Option value="h5">HDF5</Select.Option>
                            <Select.Option value="png_16">PNG 16 Bit</Select.Option>
                            <Select.Option value="png_8">PNG 8 Bit</Select.Option>
                            <Select.Option value="txt">Text</Select.Option>
                            <Select.Option value="npy">Numpy</Select.Option>
                            <Select.Option value="jpg">JPG</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="visualizationOverlay" label="Visualization Overlay?" valuePropName="checked" initialValue={false}>
                        <Switch defaultChecked={false} />
                    </Form.Item>
                </Form>
            </Modal>
        </>
    )
}
