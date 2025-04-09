import { Menu } from 'antd';
import { NavLink, useNavigate } from "react-router-dom"
import { HomeOutlined, ScissorOutlined, DatabaseOutlined, QuestionCircleOutlined, UserOutlined, LogoutOutlined } from "@ant-design/icons"

// Define the types for props
interface MenuListProps {
    darkTheme: boolean;
    updateBreadcrumb: (items: { name: string; url: string }[]) => void; // Function to update breadcrumb
}

const MenuList: React.FC<MenuListProps> = ({ darkTheme, updateBreadcrumb }) => {
    /*Component
        - switch in different dashboard function by click the navbar button
        - switch between light and dark model
    */
    const navigate = useNavigate()
    return (
        <Menu theme={darkTheme ? "dark" : "light"} mode='inline' style={{
            marginTop: "2rem",
            display: "flex",
            flexDirection: "column",
            gap: "15px",
            fontSize: "1rem",
            position: "relative"
        }}>
            <Menu.Item key="domain" icon={<HomeOutlined />}
                onClick={() => {
                    updateBreadcrumb([{ name: "Research Field", url: '/dashboard/' }])
                }}>
                <NavLink to="/dashboard/" end>
                    Research Field
                </NavLink>
            </Menu.Item>
            <Menu.Item key="trainingData" icon={<DatabaseOutlined />} onClick={() => {
                updateBreadcrumb([{ name: "Training Datasets", url: '/dashboard/dataset' }])
            }}>
                <NavLink to="/dashboard/dataset" end>
                    Training Datasets
                </NavLink>
            </Menu.Item>
            <Menu.Item key="help" icon={<QuestionCircleOutlined />}>
                <NavLink to="/dashboard/help" end>
                    Help
                </NavLink>
            </Menu.Item>
            <Menu.SubMenu key="Accout" icon={<UserOutlined />} title="Account">
                <Menu.Item key="Friends">
                    <NavLink to="/dashboard/account" onClick={() => {
                        updateBreadcrumb([{ name: "Friends", url: '/dashboard/account' }])
                    }} end>
                        Friends
                    </NavLink>
                </Menu.Item>
                <Menu.Item key="Setting">
                    <NavLink to="/dashboard" end>
                        Setting
                    </NavLink>
                </Menu.Item>
            </Menu.SubMenu>
            <Menu.Item key="logout" icon={<LogoutOutlined />}>
                <span > <a href="/api/logout"> Logout </a></span>
            </Menu.Item>
        </Menu>
    )
}

export default MenuList