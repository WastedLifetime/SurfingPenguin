import * as React from 'react';
import { withFormik, Field } from 'formik';

type Props = {
  onSubmit: func
};

const renderInput = ({field, form: { touched, errors }, ...props}) =>
    <div>
      <input {...field.input} {...field} {...props} className="form-control" />
      {
        touched[field.name] &&
        errors[field.name] &&
        <span className="help-block">{field.meta.error}</span>
      }
    </div>;

class LoginForm extends React.Component<Props> {
  render() {
    let { isSubmitting, handleSubmit, errors } = this.props;
    return (
        <form onSubmit={handleSubmit}>
          <legend>Login</legend>
          {errors.message && <div className="alert alert-danger" role="alert">{errors.message}</div>}
          <div className="form-group">
            <label htmlFor="">username</label>
            <Field
                name="username"
                component={renderInput}
                placeholder="admin@example.com"
                type="text"/>
            {this.props.values.username?<p></p>:<p className="alert alert-danger" role="alert">Username cannot be empty</p>}
          </div>
          <div className="form-group">
            <label htmlFor="">Password</label>
            <Field
                name="password"
                component={renderInput}
                placeholder="123"
                type="password"/>
            {this.props.values.password?<p></p>:<p className="alert alert-danger" role="alert">Password cannot be empty</p>}
          </div>
          {!this.props.values.password || !this.props.values.username?
          <button className="btn btn-primary" type="submit" disabled>Login</button>:
          <p>{isSubmitting ?
              <button className="btn btn-primary" type="submit" disabled>Loading...</button> :
              <button className="btn btn-primary" type="submit">Login</button>}</p>}
        </form>
    );
  }
}

export default withFormik({
  mapPropsToValues: () => {},
  handleSubmit: (values, { props, setSubmitting, setErrors }) => {
    props.onSubmit(values).then(() => {
      setSubmitting(false);

    }, (errors) => {
      setSubmitting(false);
      setErrors({

        message: errors
      })
    })
  }
})(LoginForm);
