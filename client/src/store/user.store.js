import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    user: null,
    myTheme: "light"
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setUser: (state, action) => {
            state.user = action.payload;
        },
        setUserTheme: (state, action) => {
            state.myTheme = action.payload;
        }
    },
});

export const { setUser, setUserTheme } = userSlice.actions;

export default userSlice.reducer;