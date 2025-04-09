import React, { useEffect, useState, useRef } from 'react'
import { Slider, Table, Button, Popover, Space, InputNumber } from 'antd';
import { PictureOutlined, SearchOutlined } from "@ant-design/icons";
import { Link } from 'react-router-dom'
import axios from 'axios'
import img from "../../assets/home_img2.png"


// Define types for the data being passed as props and other state variables
interface ResearchFieldData {
    id: string;
    metadata_map: Record<string, any>;  // Assuming metadata_map is a record of key-value pairs with arbitrary data
    [key: string]: any;  // To accommodate any other properties in the object
}


interface MetadataMinMax {
    [key: string]: {
        min: number;
        max: number;
        v1: number | null | undefined;
        v2: number;
    };
}

interface ColumnType {
    title: string;
    dataIndex: string | string[];
    key: string;
    render?: (text: any, record: any, index: number) => JSX.Element;
    sorter?: (a: any, b: any) => number;
    ellipsis?: boolean;
    filterDropdown?: (props: any) => JSX.Element;
    onFilter?: (value: any, record: any) => boolean;
}



export default function TableStructure({ researchFieldData }: { researchFieldData: ResearchFieldData }) {


    const [count, setCount] = useState<number>(0);
    const { metadata_map } = researchFieldData;
    // Define metadataObj as a generic object
    const metadataObj: Record<string, any> = {};
    const { id } = researchFieldData;
    // Use any as ref type since it's used dynamically
    const sliderVal = useRef<any>(null);
    // Type columns as array of ColumnType
    const [columns, setColumns] = useState<ColumnType[]>([]);
    // Data will be an array of any type (for now)
    const [data, setData] = useState<any[]>([]);
    const [metadataMinMax, setmetadataMinMax] = useState<MetadataMinMax | null>(null);

    const getColumnDataWithRange = (key: string) => ({
        filterDropdown: ({
            setSelectedKeys,
            selectedKeys,
            confirm,
            clearFilters,
            close }: any) => {
            return (
                <div
                    key={key}
                    style={{
                        padding: 8,
                    }}>
                    <div style={{ textAlign: "center" }}>
                        <InputNumber
                            min={metadataMinMax?.[key]?.min}
                            max={metadataMinMax?.[key]?.max}
                            value={metadataMinMax?.[key]?.v1}
                            onChange={(value) => {
                                setmetadataMinMax({
                                    ...metadataMinMax!, [key]: {
                                        ...[key],
                                        max: metadataMinMax![key].max,
                                        min: metadataMinMax![key].min,
                                        v1: value,
                                        v2: metadataMinMax![key].v2,
                                    }
                                });
                                confirm();
                            }} />
                        ~
                        <InputNumber
                            min={metadataMinMax?.[key]?.min}
                            max={metadataMinMax?.[key]?.max}
                            value={metadataMinMax?.[key]?.v2}
                            onChange={(value) => {
                                setmetadataMinMax({
                                    ...metadataMinMax, [key]: {
                                        max: metadataMinMax![key].max,
                                        min: metadataMinMax![key].min,
                                        v1: value,
                                        v2: metadataMinMax![key].v2,
                                    }
                                })
                                confirm();
                            }} />
                        {/* {metadataMinMax[key].v1} ~ {metadataMinMax[key].v2} */}
                    </div>
                    <Slider ref={sliderVal}
                        range
                        //@ts-ignore
                        value={[metadataMinMax?.[key]?.v1, metadataMinMax?.[key]?.v2]}
                        max={metadataMinMax?.[key]?.max}
                        min={metadataMinMax?.[key]?.min}
                        onChange={(value) => {
                            setSelectedKeys(["1"])
                            setmetadataMinMax({
                                ...metadataMinMax, [key]: {
                                    max: metadataMinMax![key].max,
                                    min: metadataMinMax![key].min,
                                    v1: value[0],
                                    v2: value[1]
                                }
                            })
                            // confirm()
                        }}
                        onChangeComplete={function (value) {
                            console.log("onChangeComplete!!!")
                            console.log("slide value: ", value);
                            setmetadataMinMax({
                                ...metadataMinMax, [key]: {
                                    max: metadataMinMax![key].max,
                                    min: metadataMinMax![key].min,
                                    v1: value[0],
                                    v2: value[1]
                                }
                            })
                            // setTestVal(?value)
                            // console.log("testVal: ", testVal)
                            confirm();

                        }} />
                    <Space style={{
                        width: 200,
                        display: "flex",
                        flexDirection: "row-reverse"
                    }}>

                        <Button
                            type="link"
                            size="small"
                            onClick={() => {
                                // setSelectedKeys([])
                                console.log("selectedKeys", selectedKeys)
                                close();
                            }}
                        >
                            close
                        </Button>
                        <Button
                            onClick={(e) => {
                                setSelectedKeys([])
                                confirm()
                                setmetadataMinMax({
                                    ...metadataMinMax, [key]: {
                                        max: metadataMinMax![key].max,
                                        min: metadataMinMax![key].min,
                                        v1: metadataMinMax![key].min,
                                        v2: metadataMinMax![key].max,
                                    }
                                })
                                // setTestVal([10, metadataMinMax[key].max])
                            }}
                            size="small"
                            style={{
                                width: 90,
                            }}>
                            Reset
                        </Button>
                    </Space>
                </div>
            )
        },
        onFilter: (value: any, record: any) => {
            let val = parseInt(record.metadata[key]);
            //@ts-ignore
            let x1 = val > metadataMinMax?.[key]?.v1;
            //@ts-ignore
            let x2 = val < metadataMinMax?.[key]?.v2;
            console.log("x1:", x1)
            console.log("x2:", x2)

            return x1 && x2;
        },
    })

    const columnInfo = [
        {
            title: 'Image Preview',
            dataIndex: 'thumbnail_path',
            key: 'thumbnail_path',
            render: (text: any, record: any, index: any) => {
                return (
                    <Popover key={index} placement="rightTop" content={
                        <div css={{
                            width: 500,
                            height: 300,
                            //@ts-ignore
                            background: `url(${import.meta.env.VITE_SRC_URL}/${record.thumbnail_path}) no-repeat center center / contain`,
                            // background: `url(http://localhost:5000/static/${record.thumbnail_path}) no-repeat center center / contain`,

                        }}>

                        </div>
                    }>
                        <PictureOutlined style={{
                            fontSize: "1.5rem",
                        }} />
                    </Popover>
                )
            },
        },
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Upload Time (UTC)',
            dataIndex: 'upload_time',
            key: 'upload_time',
        },
        {
            title: 'Creation Date (UTC)',
            dataIndex: 'creation_date',
            key: 'creation_date',
        },
        {
            title: 'Uploaded By',
            dataIndex: 'uploader_name',
            key: 'uploader_name',
        },
        {
            title: 'Size (MB)',
            dataIndex: 'size',
            key: 'size',
            sorter: (a: any, b: any) => a.size - b.size,
            // ...getColumnDataWithRange(),
        }]


    // action part 
    const columnAction = [
        {
            title: 'operation',
            dataIndex: 'operation',
            render: (_: any, record: any) => {
                return (
                    <Link to="/dashboard/crop" style={{ color: "blue" }} state={{ id: record.id, data: researchFieldData }}>
                        <Button type="primary">Crop Images</Button>
                    </Link>
                )
            }
        }
    ];

    const initializeMetadata = async () => {
        console.log("-------------------------------------------")
        // initialize metadata object
        let tempObj: any = {};
        for (const [key, value] of Object.entries(metadata_map)) {
            if (value.type == "minmax") {
                tempObj[key] = {
                    min: value.data.min,
                    max: value.data.max,
                    v1: value.data.min ?? 0,
                    v2: value.data.max,
                }
            }
        }
        await setmetadataMinMax(() => { return tempObj });
        console.log("----metadata:", metadataMinMax)

    }
    const [firstTime, setFirstTime] = useState(true)
    if (firstTime) {
        setFirstTime(false)
        initializeMetadata()
    }
    useEffect(() => {
        // setup dynamic part of data
        const columnDynamic: ColumnType[] = []
        for (const [key, value] of Object.entries(metadata_map)) {
            let tempColumn: ColumnType = {
                title: key.charAt(0).toUpperCase() + key.slice(1),
                dataIndex: ['metadata', key],
                key: key,
                ellipsis: true,
            };
            if (value.type == 'checkbox') {
                console.log("hello checkbox")
            } else if (value.type == 'minmax') {
                tempColumn = { ...tempColumn, ...getColumnDataWithRange(key) }
            }
            columnDynamic.push(tempColumn);
        }
        //@ts-ignore
        setColumns(() => { return [...columnInfo, ...columnDynamic, ...columnAction] })

        // loading data from backend 
        axios({
            // Endpoint to send files
            // url: `${import.meta.env.VITE_API_URL}dashboard`,
            url: "/api/dashboard",
            method: "GET",
            headers: {},
            // Attaching the form data
            params: { research_field_id: id }
        }).then((res) => {
            console.log("/api/dashboard res:", res)
            setData(res.data);
        }).catch((err) => { console.log(err) });
    }, [metadataMinMax])


    return (
        <Table
            size="middle"
            columns={columns}
            dataSource={data}
            pagination={{ defaultPageSize: 5 }}
        />
    )
}
