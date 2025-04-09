import React from 'react'
import { Outlet } from 'react-router-dom'
import { Nevigation, Footer } from '../../component'

export default function Layout() {
    /* Layout Page
        Layout page for homepage, <Nevigation /> component renders navbar on homepage,
        and every other pages, under homepage, will replace <Outlet /> to render itself.
    */
    return (
        <>
            <Nevigation />
            <main>
                <Outlet />
            </main>
            <Footer />
        </>
    )
}
