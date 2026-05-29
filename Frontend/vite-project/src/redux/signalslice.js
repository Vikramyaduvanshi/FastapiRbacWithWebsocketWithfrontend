import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const Fetchsignals = createAsyncThunk('signals/Fetchsignals',async (_, thunkAPI) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/general/all_signals");
            const data = await response.json();
            return data.allsignal;
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

let initialState = {
    signals: [],
    loading: false,
    error: ""
};

let Signalslice = createSlice({
    name: "signals",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
        .addCase(Fetchsignals.pending, (state, action) => {
            state.loading = true;
            state.error = "";
        })
        .addCase(Fetchsignals.fulfilled, (state, action) => {
            state.loading = false;
            state.signals = action.payload;
        })
        .addCase(Fetchsignals.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload;
        });
    }
});

export default Signalslice.reducer;


