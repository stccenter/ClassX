/*
    The last item is string, others are Link
    convert 
    list = ["Application", "Application List", "An Application"]
    to
    items={[
        {
            title: <a href="">Application Center</a>,
        },
        {
            title: <a href="">Application List</a>,
        },
        {
            title: 'An Application',
        },
        ]}
    
*/
import { Link } from 'react-router-dom'

export default function useConvertToBreadcrumb(list) {
    console.log("useConvertToBreadcrumb list:", list)
    const items = list.map((item, index) => {
        if (index != list.length - 1) {
            if (item.hasOwnProperty("state")) {
                return { title: (<Link key={index} to={item.url} state={item.state}>{item.name}</Link>) }
            } else {
                return { title: (<Link key={index} to={item.url} end>{item.name}</Link>) }
            }
        }
        return { title: item.name }
    })
    return items;
}