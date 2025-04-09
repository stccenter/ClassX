import React, { useEffect, useState } from 'react'
import styled from '@emotion/styled'
import { Space, Table, Tag, Button, Modal, Checkbox, Form, Input } from 'antd';
import { useOutletContext } from "react-router-dom";
import { useLocation } from 'react-router-dom';
import axios from 'axios'
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';
import { getOffsetLeft } from '@mui/material';
const { Column, ColumnGroup } = Table;

interface Friend {
    username: string,
    uuid: string;
    pending: boolean;
    sent: boolean
}

interface FriendIndex extends Friend {
    key: number;
}

export default function Account() {

    const [form] = Form.useForm();
    const [users, setUsers] = useState<FriendIndex[]>();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [breadcrumb, setBreadcrumb] = useOutletContext()
    const showModal = () => {
        setIsModalOpen(true);
    };

    // Fetches friends from the backend
    const fetchFriend = () => {
        axios({
            url: `/api/friends`,
            method: "GET",
        }).then((res) => {
            console.log(`/api/friends res:`, res.data)
            const data = res.data as Friend[];
            let tempUsers = data.map((item, index) => {
                return { key: index, username: item.username, uuid: item.uuid, pending: item.pending, sent: item.sent }
            });
            console.log("tempUsers: ", tempUsers)
            setUsers(tempUsers)

        }).catch((err) => { console.log(err) });
    }

    const handleOk = () => {
        console.log("form keys:", Object.keys(form.getFieldValue()))
        console.log("form:", form.getFieldValue())
        let username = form.getFieldValue("username") as string
        axios({
            url: `/api/friends`,
            method: "POST",
            params: { username: username }
        }).then((res) => {
            console.log(`/api/friends res:`, res.data)
            fetchFriend()
        }).catch((err) => { console.log(err) });
        setIsModalOpen(false);
    };
    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const deleteUser = (uuid: string) => {
        console.log("delete user uuid: ", uuid)
        axios({
            url: `/api/friends`,
            method: "DELETE",
            params: { uuid: uuid }
        }).then((res) => {
            console.log(`/api/friends res:`, res.data)
            fetchFriend();
        }).catch((err) => { console.log(err) });
    }

    const handleAcceptRequest = (uuid: string) => {
        axios({
            url: `/api/friends`,
            method: "PATCH",
            params: { uuid: uuid }
        }).then((res) => {
            console.log(`/api/friends res:`, res.data)
            fetchFriend();
        }).catch((err) => { console.log(err) });
    }
    useEffect(() => {
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Friends", url: "/dashboard/" }]));
        fetchFriend();
    }, [])
    return (
        <Container>
            <Button type="primary" onClick={showModal} style={{ margin: "1rem" }}>
                Add Friend
            </Button>
            <Modal title="Add Friend" open={isModalOpen} onCancel={handleCancel}
                footer={[
                    <Button key="back" onClick={handleCancel}>
                        Cancel
                    </Button>,
                    <Button key="submit" type="primary" onClick={handleOk} >
                        Search
                    </Button>,
                ]}
            >
                <Form
                    name="basic"
                    labelCol={{
                        span: 6,
                    }}
                    wrapperCol={{
                        span: 16,
                    }}
                    style={{
                        maxWidth: 600,
                    }}
                    initialValues={{
                        remember: true,
                    }}
                    form={form}
                >
                    <Form.Item
                        label="Username"
                        name="username"
                    >
                        <Input />
                    </Form.Item>
                </Form>
            </Modal>
            <Table dataSource={users}>
                <Column title="Username" dataIndex="username" key="username" />
                <Column
                    title="State"
                    dataIndex="tags"
                    key="tags"
                    render={(_, record) => (

                        record.pending ?
                            <Tag color="gold">Waiting</Tag> :
                            <Tag color="green">Accept</Tag>

                    )
                    }
                />
                <Column
                    title="Action"
                    key="action"
                    render={(_, record) => (
                        record.sent || record == undefined ?

                            <Space size="middle">
                                <Button onClick={() => { deleteUser(record.uuid) }}>Delete</Button>
                            </Space> :
                            <Space size="middle">
                                <Button onClick={() => { handleAcceptRequest(record.uuid) }} type="primary">Accept</Button>
                                <Button onClick={() => { deleteUser(record.uuid) }} danger>Reject</Button>
                            </Space>
                    )}
                />
            </Table>
        </Container >
    )
}
const Container = styled.div`
    height:92vh;
`