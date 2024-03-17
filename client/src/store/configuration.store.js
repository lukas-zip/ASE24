import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    collapsed: localStorage.getItem('collapsed') === 'true' || false,
}

export const configurationSlice = createSlice({
    name: 'configuration',
    initialState,
    reducers: {
        setCollapsed: (state, action) => {
            localStorage.setItem('collapsed', action.payload)
            state.collapsed = action.payload;
        },
    },
});
export const { setCollapsed } = configurationSlice.actions;

export default configurationSlice.reducer;