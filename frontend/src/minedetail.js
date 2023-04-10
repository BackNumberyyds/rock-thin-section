import React from 'react';
import ReactDOM from "react-dom/client";
import { LayerChart, SampleNameChart } from './mine-detail/charts'

const rootElement = document.getElementById("layer_chart");
fetch("/api" + window.location.pathname)
    .then(response => response.json())
    .then(data => {
        ReactDOM.createRoot(rootElement).render(<LayerChart data={data.layer_data} />);
    });
// ReactDOM.createRoot(rootElement).render(<SampleNameChart />);
