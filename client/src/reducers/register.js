export default function (state = {isSuccess: false, isLoading: false}, action) {
  console.log(action.type)
  switch (action.type) {
    case 'REGISTER_REQUEST':
      return {
        ...state,
        isLoading: true
      }
    case 'REGISTER_REQUEST_SUCCESS':
      return {
        ...state,
        isLoading: false,
        isSuccess: true
      }
    case 'REGISTER_REQUEST_FAIL':
      return {
        ...state,
        isLoading: false,
        isSuccess: false
      }
    case 'REGISTER_REQUEST_FAIL_DUPLICATE_USERNAME':
      return {
        ...state,
        isLoading: false,
        isSuccess: false
      }
    default:
      return state
  }
};
