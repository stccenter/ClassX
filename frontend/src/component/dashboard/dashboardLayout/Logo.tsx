import React from 'react'
import { FireFilled } from '@ant-design/icons'
import ClassXLogo from "../../../assets/logo.png"

export default function Logo() {
    /*Component
        Logo component on dashboard
    */
    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            padding: "10px"
        }}>
            <div style={{
                width: "80px",
                height: "80px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "1.5rem",
                borderRadius: "50%",
                background: "rgba(28,17,41,0.88)"
            }}>
                <img src={ClassXLogo} alt="" style={{ height: "70%" }} />
            </div>
        </div>
    )
}
