import React, { useState, useEffect } from 'react'
import { Button, Modal } from "antd"
import axios from "axios"

export default function ViewViewButton() {

    const [isModalOpen, setIsModalOpen] = useState(false);
    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    useEffect(() => {
        // axios({
        //     // Endpoint to send files
        //     url: "/api/getTrainingFileContents/",
        //     method: "GET",
        //     headers: {},
        // }).then((res) => {
        //     console.log("/api/getTrainingFileContents/", res)
        // }).catch((err) => { console.log(err) });
    }, [])
    return (
        <>
            <Button onClick={showModal}>View</Button>
            <Modal title="Basic Modal" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                hello

            </Modal>
        </>
    )
}
