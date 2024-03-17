import { useMemo } from 'react'
import { useDispatch, useSelector } from 'react-redux'

const useUserTheme = () => {
    const { myTheme } = useSelector(state => state.user)
    const userTheme = useMemo(() => {
        return myTheme
    }, [myTheme])

    // return userTheme
    return "light"
}

export default useUserTheme