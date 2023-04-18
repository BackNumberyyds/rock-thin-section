import React from 'react';
import ReactDOM from "react-dom/client";
import { LayerChart, SampleNameChart, RockCompositionChart } from './mine-detail/charts'

const LayerChartElement = document.getElementById("layer_chart");
const SampleNameElement = document.getElementById("sample_name_chart");
const RockCompositionElement = document.getElementById("rock_composition_chart");
fetch("/api" + window.location.pathname)
    .then(response => response.json())
    .then(data => {
        ReactDOM.createRoot(LayerChartElement).render(<LayerChart data={data.layer_data} />);
        ReactDOM.createRoot(SampleNameElement).render(<SampleNameChart data={data.sample_name_data} />);
        ReactDOM.createRoot(RockCompositionElement).render(<RockCompositionChart data={data.sample_composition_data.data} />);
    });
