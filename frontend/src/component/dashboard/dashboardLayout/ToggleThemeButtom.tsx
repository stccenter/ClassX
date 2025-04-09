import React from 'react'
import { Button } from 'antd'
import { HiOutlineSun, HiOutlineMoon } from "react-icons/hi"

// Define the types for the props
interface ToggleThemeButtonProps {
    darkTheme: boolean;
    toggleTheme: () => void;
}

const ToggleThemeButtom: React.FC<ToggleThemeButtonProps> = ({ darkTheme, toggleTheme }) => {
    /*Component 
        theme switch button
    */

    return (
        <div style={{
            position: "absolute",
            bottom: "30px",
            left: "20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "1rem"
        }}>
            <Button onClick={toggleTheme}>
                {darkTheme ? <HiOutlineSun /> : <HiOutlineMoon />}
            </Button>
        </div>
    )
}

export default ToggleThemeButtom