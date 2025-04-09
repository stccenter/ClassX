import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { Home, Pricing, Contact, Layout, DLayout, ResearchField, Account, Help, Dataset, Segment, ViewImage, Crop, Images } from './pages'
import './App.css'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route path="/" element={<Home />} />
                    {/* <Route path="/pricing" element={<Pricing />} /> remove pricing */}
                    <Route path="/contact" element={<Contact />} />
                </Route>
                <Route path="/dashboard" element={<DLayout />}>
                    <Route path="/dashboard/" element={<ResearchField />} />
                    <Route path="/dashboard/segment" element={<Segment />} />
                    <Route path="/dashboard/crop" element={<Crop />} />
                    <Route path="/dashboard/account" element={<Account />} />
                    <Route path="/dashboard/dataset" element={<Dataset />} />
                    <Route path="/dashboard/help" element={<Help />} />
                    <Route path="/dashboard/images" element={<Images />} />
                    <Route path="/dashboard/viewimage" element={<ViewImage />} />
                </Route>
            </Routes>

        </Router>
    )
}


export default App
