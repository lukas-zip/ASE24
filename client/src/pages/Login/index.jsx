import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './index.less'
import { shallowEqual, useDispatch, useSelector } from 'react-redux'
import { Radio, message } from 'antd'
import { setUser } from '../../store/user.store'
import { signIn, signUpForUser, signUpForShop } from '../../api/user.api'
import PROJECT_VARIABLE from '../../constants/ProjectNameVariable'
import CONSTANTS from '../../constants'

export default function Login() {
    const { user } = useSelector(state => state.user, shallowEqual)
    const navigateTo = useNavigate()
    const dispatch = useDispatch()
    const [signup, setSignup] = useState(false)
    const [focusedname, setFocusedname] = useState(false)
    const [focusedpassword, setFocusedpassword] = useState(false)
    const [focusednameSup, setFocusednameSup] = useState(false)
    const [focusedpasswordSup, setFocusedpasswordSup] = useState(false)
    const [focusedemail, setFocusedemail] = useState(false)
    const [selectedPic, setSelectedPic] = useState(1)
    const [sigInInfo, setSignInInfo] = useState({})
    const activename = focusedname ? 'active' : ''
    const activepassword = focusedpassword ? 'active' : ''

    const [sigUpInfo, setSignUpInfo] = useState({})
    const activenameSup = focusednameSup ? 'active' : ''
    const activepasswordSup = focusedpasswordSup ? 'active' : ''
    const activeemail = focusedemail ? 'active' : ''
    useEffect(() => {
        const timer = window.setInterval(() => {
            setSelectedPic((prev) => {
                return prev !== 5 ? prev + 1 : 1
            })
        }, 3000);
        return () => {
            clearInterval(timer);
        };
    }, []);
    useEffect(() => {
        user && navigateTo('/')
    }, [user])

    const UserSignIn = async () => {
        await signIn(sigInInfo).then(res => {
            if (res.status) {
                localStorage.setItem('user', res.value)
                dispatch(setUser(res.value))
                navigateTo('/')
            } else {
                message.error(res.message.message)
            }
        }).catch(err => {
            message.error('Error happen, try again please')
        })
    }
    const [role, setRole] = useState(CONSTANTS.USER_TYPE.USER)

    const registerUser = async () => {
        const { name, email, password } = sigUpInfo
        if (role === CONSTANTS.USER_TYPE.USER) {
            const reqData = {
                email,
                password,
                username: name,
                address: "",
                phone: ""
            }
            await signUpForUser(reqData)
                .then((res) => {
                    if (res.status) {
                        dispatch(setUser(res.value))
                        navigateTo('/')
                        message.success('Register Successfully! Have a nice trip!!!')
                    } else {
                        console.log(res.message);
                        message.error(res.message)
                    }
                })
                .catch((err) => {
                    console.log(err);
                    message.error('Registration Failure! Try again please')
                })
        } else if (role === CONSTANTS.USER_TYPE.SHOP) {
            const reqData = {
                email,
                password,
                shop_name: name,
                description: '',
                address: "",
                phone: ""
            }
            await signUpForShop(reqData)
                .then((res) => {
                    if (res.status === true) {
                        dispatch(setUser(res.value))
                        navigateTo('/')
                        message.success('Register Successfully! Have a nice trip!!!')
                    } else {
                        console.log("zheli", res);
                        message.error(res.message.message)
                        console.log("zheli");
                    }
                })
                .catch((err) => {
                    console.log(err);
                    message.info('Registration Failure! Try again please')
                })
        }
    }

    return (

        <div className={`Login_mainBox ${signup ? 'sign-up-mode' : ''}`}>
            <div className='box'>
                <div className='inner-box'>
                    <div className='forms-wrap'>
                        <form onSubmit={(e) => {
                            e.preventDefault()
                            UserSignIn()
                        }} autoComplete="off" className='sign-in-form'>
                            <div className='logo'>
                                {/* img */}
                                <h4>{PROJECT_VARIABLE.PROJECT_NAME}</h4>
                            </div>
                            <div className='heading'>
                                <h2>Welcome Back</h2>
                                <h6>Not registered yet?</h6>
                                <a className='toggle' onClick={() => setSignup(true)}>&nbsp;Sign up</a>
                            </div>
                            <div className='actual-form'>
                                <div className='input-wrap'>
                                    <input
                                        type='email'
                                        minLength={4}
                                        onFocus={() => setFocusedpassword(true)}
                                        onBlur={({ target: { value } }) => {
                                            if (value != "") {
                                                return;
                                            }
                                            setFocusedpassword(false)
                                        }}
                                        onChange={({ target: { value } }) => setSignInInfo({ ...sigInInfo, email: value })}
                                        // onChange={({ target: { value } }) => setSignInInfo({ ...sigInInfo, email: value })}
                                        className={`input-field ${activepassword}`}
                                        autoComplete="off"
                                        required
                                    />
                                    <label>Email</label>
                                </div>
                                <div className='input-wrap'>
                                    <input
                                        type='password'
                                        minLength={4}
                                        className={`input-field ${activename}`}
                                        onFocus={() => setFocusedname(true)}
                                        onBlur={({ target: { value } }) => {
                                            if (value != "") {
                                                return;
                                            }
                                            setFocusedname(false)
                                        }}
                                        onChange={({ target: { value } }) => setSignInInfo({ ...sigInInfo, password: value })}
                                        autoComplete="off"
                                        required
                                    />
                                    <label>Password</label>
                                </div>
                                <input type='submit' value="Sign In" className='sign-btn' />
                            </div>
                        </form>

                        <form onSubmit={(e) => {
                            e.preventDefault()
                            registerUser()
                        }} autoComplete="off" className='sign-up-form'>
                            <div className='logo'>
                                {/* img */}
                                <h4>{PROJECT_VARIABLE.PROJECT_NAME}</h4>
                            </div>
                            <div className='heading'>
                                <h2>Start</h2>
                                <h6>Already have account</h6>
                                <a className='toggle' onClick={() => setSignup(false)}>&nbsp;Sign In</a>
                            </div>
                            <div>
                                <label style={{ marginRight: 6 }}>Enrol as: </label>
                                <Radio.Group defaultValue={role} onChange={({ target: { value } }) => setRole(value)}>
                                    <Radio.Button value={CONSTANTS.USER_TYPE.USER}>User</Radio.Button>
                                    <Radio.Button value={CONSTANTS.USER_TYPE.SHOP}>Shop</Radio.Button>
                                </Radio.Group>
                            </div>
                            <div className='actual-form'>
                                <div className='input-wrap'>
                                    <input
                                        type='text'
                                        minLength={4}
                                        className={`input-field ${activenameSup}`}
                                        onFocus={() => setFocusednameSup(true)}
                                        onBlur={({ target: { value } }) => {
                                            if (value != "") {
                                                return;
                                            }
                                            setFocusednameSup(false)
                                        }}
                                        onChange={({ target: { value } }) => setSignUpInfo({ ...sigUpInfo, name: value })}
                                        autoComplete="off"
                                        required
                                    />
                                    <label>Name</label>
                                </div>
                                <div className='input-wrap'>
                                    <input
                                        type='email'
                                        minLength={4}
                                        className={`input-field ${activeemail}`}
                                        onFocus={() => setFocusedemail(true)}
                                        onBlur={({ target: { value } }) => {
                                            if (value != "") {
                                                return;
                                            }
                                            setFocusedemail(false)
                                        }}
                                        onChange={({ target: { value } }) => setSignUpInfo({ ...sigUpInfo, email: value })}
                                        autoComplete="off"
                                        required
                                    />
                                    <label>Email</label>
                                </div>
                                <div className='input-wrap'>
                                    <input
                                        type='password'
                                        minLength={4}
                                        onFocus={() => setFocusedpasswordSup(true)}
                                        onBlur={({ target: { value } }) => {
                                            if (value != "") {
                                                return;
                                            }
                                            setFocusedpasswordSup(false)
                                        }}
                                        className={`input-field ${activepasswordSup}`}
                                        autoComplete="off"
                                        onChange={({ target: { value } }) => setSignUpInfo({ ...sigUpInfo, password: value })}
                                        required
                                    />
                                    <label>Password</label>
                                </div>
                                <input type='submit' value={"Sigin up"} className='sign-btn' />
                            </div>
                        </form>
                    </div>
                    <div className='carousel'>
                        <div className='images-wrapper'>
                            {PROJECT_VARIABLE.PROJECT_PROMO.map(item => <img key={`promoPic${item.id}`} src={item.pic} className={`image img-${item.id} ${selectedPic === item.id && "show"}`}></img>)}
                        </div>
                        <div className='text-slider'>
                            <div className='text-wrap'>
                                <div className='text-group' style={{ transform: `translateY(${-(selectedPic - 1) * 2.2}rem)` }}>
                                    {PROJECT_VARIABLE.PROJECT_PROMO.map(item => <h2 key={`promoTitle${item.id}`}>{item.title}</h2>)}
                                </div>
                            </div>
                            <div className='bullets'>
                                <span className={selectedPic === 1 ? `active` : ''} onClick={() => setSelectedPic(1)}></span>
                                <span className={selectedPic === 2 ? `active` : ''} onClick={() => setSelectedPic(2)}></span>
                                <span className={selectedPic === 3 ? `active` : ''} onClick={() => setSelectedPic(3)}></span>
                                <span className={selectedPic === 4 ? `active` : ''} onClick={() => setSelectedPic(4)}></span>
                                <span className={selectedPic === 5 ? `active` : ''} onClick={() => setSelectedPic(5)}></span>
                            </div>
                        </div>
                    </div>
                </div >
            </div >
        </div >
    )
}
