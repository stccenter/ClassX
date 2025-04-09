import React from 'react'
import { Slide, ProductIntro, Aboutus } from "../../component"


export default function Home() {
    /*Page
        The first page user enter classX tool. 
        <Slide /> switch different image on top side
        <ProductionIntro /> introduce the basic idea about classX tool
        <Aboutus /> shows classX team
    */
    return (
        <>
            <Slide />
            <ProductIntro />
            <Aboutus />
        </>
    );
}




