import React, { useState, useEffect } from 'react'
import { Button, Modal, Form, Checkbox } from 'antd'
import { ShareAltOutlined } from "@ant-design/icons";
import axios from 'axios'

export default function viewShareButton(props) {
    const { record } = props;
    console.log("record:", record)
    const [form] = Form.useForm();
    const [friendList, setFriendList] = useState(null)
    const [isModalOpen, setIsModalOpen] = useState(false);

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        console.log("form:", Object.keys(form.getFieldValue()))
        let data = JSON.stringify({
            'training_file_id': record.id,
            'recipient_name_list': Object.keys(form.getFieldValue())
        })
        console.log("data:", data)
        axios.post("/api/shareTrainingFileToUsers/", data, {
            headers: {
                'Content-Type': 'application/json',
            }
        }).then((res) => {
            console.log("/api/shareTrainingFileToUsers/", res)
            //NOTIFICATION
        }).catch((err) => { console.log(err) });
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };
    useEffect(() => {
        axios({
            // Endpoint to send files
            url: "/api/getUserShareList/",
            method: "GET",
            headers: {},
        }).then((res) => {
            console.log("/api/getUserShareList/", res)
            let tempFriendList = res.data.username_list.map(item => {
                return (
                    <Form.Item name={item} valuePropName="checked" initialValue={false} >
                        <Checkbox defaultChecked={false}>{item}</Checkbox>
                    </Form.Item >
                )
            })
            setFriendList(tempFriendList)
        }).catch((err) => { console.log(err) });
    }, [])
    return (
        <>
            <Button onClick={showModal} >Share</Button>
            <Modal title="Basic Modal"
                open={isModalOpen} onCancel={handleCancel}
                footer={[
                    <Button key="back" onClick={handleCancel}>
                        Cancel
                    </Button>,
                    <Button key="submit" type="primary" onClick={handleOk}>
                        Submit
                    </Button>,
                ]}>
                <Form
                    labelCol={{
                        span: 4,
                    }}
                    wrapperCol={{
                        span: 14,
                    }}
                    onFinish={handleOk}
                    form={form}
                    layout="horizontal"
                    style={{
                        maxWidth: 600,
                    }}
                >
                    {friendList}
                </Form>

            </Modal>
        </>
    )
}
