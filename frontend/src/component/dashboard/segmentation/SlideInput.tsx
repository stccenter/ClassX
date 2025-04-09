import React, { useState } from 'react';
import { Col, InputNumber, Row, Slider, Space } from 'antd';

export default function SlideInput(props) {
    // console.log("props:", props)
    const { min, max, step, defaultValue, setValue } = props;
    const [inputValue, setInputValue] = useState(defaultValue);
    const onChange = (newValue) => {
        setInputValue(newValue);
        setValue(newValue);
    };
    return (
        <Row>
            <Col span={12}>
                <Slider
                    min={min}
                    max={max}
                    onChange={onChange}
                    step={step}
                    value={typeof inputValue === 'number' ? inputValue : 0}
                />
            </Col>
            <Col span={4}>
                <InputNumber
                    min={min}
                    max={max}
                    style={{
                        margin: '0 16px',
                    }}
                    step={step}
                    value={inputValue}
                    onChange={onChange}
                />
            </Col>
        </Row>
    );
}
