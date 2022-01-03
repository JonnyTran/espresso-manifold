from torch import Tensor


def tensor_sizes(input):
    if isinstance(input, dict):
        return {metapath if not isinstance(metapath, tuple) else \
                    ".".join([type[0].upper() if i % 2 == 0 else type[0].lower() for i, type in
                              enumerate(metapath)]): tensor_sizes(v) \
                for metapath, v in input.items()}
    elif isinstance(input, tuple):
        return tuple(tensor_sizes(v) for v in input)
    elif isinstance(input, list):
        return [tensor_sizes(v) for v in input]
    else:
        if input is not None and hasattr(input, "shape"):
            if isinstance(input, Tensor) and input.dim() == 0:
                return input.item()

            return list(input.shape)
        else:
            return input