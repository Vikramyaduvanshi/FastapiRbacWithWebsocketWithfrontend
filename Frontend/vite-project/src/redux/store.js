import { configureStore } from "@reduxjs/toolkit";
import SignalsReducer from "./signalslice.js";

export const store = configureStore({
    reducer: {
        signals: SignalsReducer
    }

});