import React, { useState, useEffect } from 'react';
import { Outlet, Link } from 'react-router-dom'
import { Button, Layout, theme, Breadcrumb } from 'antd';
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons"
import { Logo, MenuList, ToggleThemeButtom } from "../../component"
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb'

// Get Header and Sider component from Layout
const { Header, Sider } = Layout;

// Define types for the breadcrumb item that Ant Design expects
interface BreadcrumbItemType {
    title: string;
    href?: string;
}

// Define types for the breadcrumb item
interface BreadcrumbItem {
    name: string;
    url: string;
}

const App: React.FC = () => {
    /*Page
        Set up the basic layout for dashboard
    */

    // State declaration
    const [darkTheme, setDarkTheme] = useState<boolean>(true)
    const [collapsed, setCollapsed] = useState<boolean>(false)
    const [breadcrumb, setBreadcrumb] = useState<BreadcrumbItemType[]>([])

    // toggle theme switch between light and dark
    const toggleTheme = () => {
        setDarkTheme(!darkTheme);
    }
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    // update breadcrumb by items
    const updateBreadcrumb = (item: BreadcrumbItem[]) => {
        setBreadcrumb(useConvertToBreadcrumb(item))
    }

    // on component render
    useEffect(() => {
        // set up breadcrumb
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Research Field", url: "/dashboard/" }]))
    }, [])

    return (
        <Layout>
            <Sider
                collapsed={collapsed}
                collapsible
                trigger={null}
                theme={darkTheme ? "dark" : "light"}
                style={{ color: "#fff" }}>
                <Logo />
                <MenuList darkTheme={darkTheme} updateBreadcrumb={updateBreadcrumb} />
                <ToggleThemeButtom darkTheme={darkTheme} toggleTheme={toggleTheme} />
            </Sider>
            <Layout>
                <Header style={{
                    padding: 0,
                    background: colorBgContainer,
                    display: 'flex',
                    alignItems: 'center',
                    height: "8vh"
                }}>
                    <Button
                        type="text"
                        style={{
                            marginLeft: "15px",
                            marginRight: "15px"
                        }}
                        onClick={() => setCollapsed(!collapsed)}
                        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} >
                    </Button>
                    <Breadcrumb
                        items={breadcrumb}
                    />
                </Header>
                <main>
                    <Outlet context={[breadcrumb, setBreadcrumb]} />
                </main>
            </Layout>
        </Layout >

    );
};
export default App;