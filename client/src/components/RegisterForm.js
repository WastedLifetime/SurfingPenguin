import * as React from 'react'
import { Field, withFormik } from 'formik'

const renderInput = ({field, form: { touched, errors }, ...props}) =>
  <div>
    <input {...field.input} {...field} {...props} className='form-control' />
    {
      errors[field.name] &&
        <span className='text-danger help-block'>{errors[field.name].join(' ')}</span>
    }
  </div>
type Props = {
  onSubmit: Function
};

class RegisterForm extends React.Component<Props> {
  render () {
    let {isSubmitting, handleSubmit, errors, touched} = this.props
    return (
      <form onSubmit={handleSubmit}>
        <legend>Register</legend>
        {errors.message && <div className='alert alert-danger' role='alert'>{errors.message}</div>}
        <div className='form-group'>
          <label htmlFor=''>User Name</label>
          <Field
            name='username'
            component={renderInput}
            form={{errors, touched}}
            type='text' />
          {!this.props.values.username && touched.username
            ? <p className='alert alert-danger' role='alert'>Username cannot be empty</p>
            : <p />}
        </div>
        <div className='form-group'>
          <label htmlFor=''>Password</label>
          <Field
            name='password'
            component={renderInput}
            type='password' />
          {!this.props.values.password && touched.password
            ? <p className='alert alert-danger' role='alert'>Password cannot be empty</p>
            : <p />}
        </div>
        <div className='form-group'>
          <label htmlFor=''>Confirm Password</label>
          <Field
            name='passwordConfirm'
            component={renderInput}
            type='password' />
          {this.props.values.password !== this.props.values.passwordConfirm
            ? <p className='alert alert-danger' role='alert'>Different password</p>
            : <p />}
        </div>
        {this.props.values.password !== this.props.values.passwordConfirm || !this.props.values.password || !this.props.values.username
          ? <button className='btn btn-primary' type='submit' disabled>Submit</button>
          : <p>{isSubmitting
            ? <button className='btn btn-primary' type='submit' disabled>Loading...</button>
            : <button className='btn btn-primary' type='submit'>Submit</button>}</p>}
      </form>
    )
  }
}
export default withFormik({
  mapPropsToValues: () => {},
  handleSubmit: (values, { props, setSubmitting, setErrors }) => {
    props.onSubmit(values).then(() => {
      setSubmitting(false)
    }, (errors) => {
      setSubmitting(false)
      if (typeof (errors) !== 'string') {
        setErrors({message: 'Network Error'})
      } else {
        setErrors({message: errors})
      }
    })
  }
})(RegisterForm)
