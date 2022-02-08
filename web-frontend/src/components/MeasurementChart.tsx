import * as React from 'react';
import { useTheme, Typography } from '@mui/material';
import {
    LineChart, ComposedChart, Bar, Line, XAxis, YAxis, Label,
    ResponsiveContainer, CartesianGrid,
    Tooltip, Legend
} from 'recharts';
import moment from 'moment'


type Point = {
    tstamp?: string,
    acc_x?: number,
    acc_y?: number,
    acc_z?: number,
    run_time?: number,
}

type Measure = {
    name: string,
    unit: string,
    startDate: string,
    endDate: string,
    points: Array<Point>,
}

function getVibrationalData(measurements: any) {
    let dataLen = Math.min(...measurements.map((m: any) => m.data.length));
    let measures = Array<Point>(dataLen);
    for (var i = 0; i < dataLen; i++) {
        let point: Point = {};
        for (var measure of measurements) {
            let p = measure.data[i];
            switch (measure.info.measurementTypeId) {
                case 31:
                    point.acc_x = p.value;
                    point.tstamp = moment(new Date(p.timestamp)).format('DD/MM/YY - HH:mm');
                    break;
                case 32: point.acc_y = p.value; break;
                case 33: point.acc_z = p.value; break;
                case 209: point.run_time = p.value; break;
            }
        }
        measures[i] = point;
    }
    return measures;
}

interface TitleProps {
    children?: React.ReactNode;
}

function Title(props: TitleProps) {
    return (
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
            {props.children}
        </Typography>
    );
}

const CustomTooltip = ({
    active,
    payload,
    label,
    coordinate,
    ...props
}: any) => {
    if (active && payload?.length) {
        return (
            <div className="customTooltip">
                <p className="label">{'' + new Date(label)}</p>
                {payload.map((v: any, index: number) => {
                    return <p className="label" key={index}>{`${v.name}: ${v.value}`}</p>
                })}
            </div>
        );
    }
    return null;
}

export default function Chart(props: { data: any }) {
    const theme = useTheme();
    const data = props.data; // getVibrationalData(props.data);
    return (
        <React.Fragment>
            <Title>Mese scorso</Title>
            <ResponsiveContainer>
                <ComposedChart
                    data={data}
                    margin={{
                        top: 16,
                        right: 16,
                        bottom: 0,
                        left: 24,
                    }}
                >
                    <XAxis
                        dataKey="tstamp"
                        stroke={theme.palette.text.secondary}
                        style={theme.typography.body2}
                        // tickCount={2}
                        tickFormatter={(date) => date.split('/')[0]}
                    // type='number'
                    // domain={['auto', 'auto']}
                    />
                    <YAxis
                        stroke={theme.palette.text.secondary}
                        style={theme.typography.body2}
                        yAxisId="left"
                    >
                        <Label
                            angle={270}
                            position="left"
                            style={{
                                textAnchor: 'middle',
                                fill: theme.palette.text.primary,
                                ...theme.typography.body1,
                            }}
                        >
                            Vibrazioni - mm/s
                        </Label>
                    </YAxis>
                    <YAxis
                        stroke={theme.palette.text.secondary}
                        style={theme.typography.body2}
                        orientation="right"
                        yAxisId="right"

                    >
                        <Label
                            angle={270}
                            position="right"
                            style={{

                                textAnchor: 'middle',
                                fill: theme.palette.text.primary,
                                ...theme.typography.body1,
                            }}
                        >
                            Funzionamento - min
                        </Label>
                    </YAxis>
                    <Legend />
                    <Tooltip />
                    <CartesianGrid />
                    <Bar
                        yAxisId="right"
                        name="Funzionamento"
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="run_time"
                        stroke="#ccc"
                        fill="#333"
                    />
                    <Line
                        yAxisId="left"
                        name="Assiale"
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="acc_x"
                        stroke={theme.palette.primary.main}
                        dot={false}
                    />
                    <Line
                        yAxisId="left"
                        name="Radiale"
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="acc_y"
                        stroke="#8884d8"
                        dot={false}
                    />
                    <Line
                        yAxisId="left"
                        name="Tangenziale"
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="acc_z"
                        stroke={theme.palette.secondary.main}
                        dot={false}
                    />
                </ComposedChart>
            </ResponsiveContainer>
        </React.Fragment >
    );
}